import sys
import copy
import json
import traceback

MAX_FRAMES = 1000

def generate_python_trace(code: str):
    """
    Executes Python code securely in a restricted dictionary scope and generates an execution trace.
    Returns a dict with {"frames": [...], "error": None, "totalSteps": count}
    """
    frames = []
    
    # Safe environment
    global_env = {"__builtins__": __builtins__}
    local_env = {}
    
    op_count = [0]
    error_msg = None
    
    def sanitize_val(v):
        """Convert objects to JSON serializable structures."""
        if isinstance(v, (int, float, str, bool, type(None))):
            return v
        elif isinstance(v, list):
            return [sanitize_val(item) for item in v[:50]]
        elif isinstance(v, dict):
            return {str(k): sanitize_val(val) for k, val in list(v.items())[:50]}
        elif isinstance(v, tuple):
            return [sanitize_val(item) for item in v[:50]]
        else:
            return f"<{type(v).__name__}>"

    def trace_callback(frame, event, arg):
        if frame.f_code.co_filename != "<string>":
            return trace_callback

        if event == 'line':
            op_count[0] += 1
            if op_count[0] > MAX_FRAMES:
                raise RuntimeError(f"Execution Limit Exceeded (Max {MAX_FRAMES} frames). Possible infinite loop.")
            
            # Extract variables safely
            variables = {}
            pointers = {}
            array_obj = None
            stack_obj = None
            queue_obj = None
            hash_maps = []
            dp_table = None
            memory_list = []

            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    sanitized = sanitize_val(v)
                    addr = (id(v) % 100000)
                    variables[k] = {
                        "type": type(v).__name__,
                        "value": sanitized,
                        "address": addr,
                        "changed": False
                    }
                    memory_list.append({
                        "name": k,
                        "type": type(v).__name__,
                        "value": sanitized,
                        "address": f"0x{addr:05X}",
                        "changed": False
                    })

                    # Detect integer pointers
                    if isinstance(v, int) and k in ['left', 'right', 'mid', 'low', 'high', 'i', 'j', 'k', 'p1', 'p2', 'head', 'tail']:
                        pointers[k] = v

                    # Detect primary array/list
                    if isinstance(v, list) and not array_obj and k not in ['stack', 'queue', 'stk', 'q']:
                        # Check if 2D list (DP matrix)
                        if len(v) > 0 and isinstance(v[0], list):
                            dp_table = {
                                "name": k,
                                "matrix": sanitized,
                                "activeCell": None
                            }
                        else:
                            array_obj = {
                                "name": k,
                                "values": sanitized,
                                "pointers": copy.deepcopy(pointers)
                            }
                    
                    # Detect stack
                    if isinstance(v, list) and ('stack' in k.lower() or 'stk' in k.lower()):
                        stack_obj = {
                            "name": k,
                            "values": sanitized
                        }

                    # Detect queue
                    if isinstance(v, list) and ('queue' in k.lower() or 'q' in k.lower()):
                        queue_obj = {
                            "name": k,
                            "values": sanitized,
                            "front": 0,
                            "rear": len(v) - 1 if len(v) > 0 else 0
                        }

                    # Detect dict/hash map
                    if isinstance(v, dict):
                        hash_maps.append({
                            "name": k,
                            "entries": sanitized
                        })

            # Check for changed variables
            if frames and "variables" in frames[-1]:
                prev_vars = frames[-1]["variables"]
                for k, v_data in variables.items():
                    if k not in prev_vars or prev_vars[k]["value"] != v_data["value"]:
                        v_data["changed"] = True
                        for m in memory_list:
                            if m["name"] == k:
                                m["changed"] = True

            # If array_obj exists, keep pointers updated
            if array_obj:
                array_obj["pointers"] = pointers

            # Calculate call stack depth
            depth = 0
            f = frame
            call_stack = []
            while f and f.f_code.co_filename == "<string>":
                call_stack.append(f.f_code.co_name)
                depth += 1
                f = f.f_back
            
            explanation_str = f"Executing Line {frame.f_lineno}"
            if pointers:
                p_str = ", ".join([f"{pk}={pv}" for pk, pv in pointers.items()])
                explanation_str += f" ({p_str})"

            frame_data = {
                "step": op_count[0],
                "line": frame.f_lineno,
                "highlightedLine": frame.f_lineno,
                "variables": variables,
                "callStack": call_stack[::-1],
                "memory": memory_list,
                "array": array_obj,
                "arrays": [array_obj] if array_obj else [],
                "stack": stack_obj,
                "queue": queue_obj,
                "hashMaps": hash_maps,
                "dpTable": dp_table,
                "linkedList": None,
                "tree": None,
                "graph": None,
                "heap": None,
                "output": "",
                "condition": None,
                "loopIteration": op_count[0],
                "explanation": explanation_str,
                "edgeCase": None,
                "complexity": {
                    "opCount": op_count[0],
                    "comparisons": 0,
                    "swaps": 0,
                    "depth": depth
                }
            }
            frames.append(frame_data)
        
        return trace_callback

    try:
        compiled_code = compile(code, "<string>", "exec")
        
        sys.settrace(trace_callback)
        try:
            exec(compiled_code, global_env, local_env)
        finally:
            sys.settrace(None)
            
    except RuntimeError as e:
        error_msg = str(e)
    except SyntaxError as e:
        error_msg = f"Compilation Error: {e.msg} on line {e.lineno}"
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        for t in reversed(tb):
            if t.filename == "<string>":
                error_msg = f"Runtime Error on line {t.lineno}: {type(e).__name__}: {str(e)}"
                break
        if not error_msg:
            error_msg = f"Runtime Error: {type(e).__name__}: {str(e)}"

    # Append terminal frame if an error occurred
    if error_msg:
        frames.append({
            "step": op_count[0] + 1,
            "line": 1,
            "highlightedLine": 1,
            "variables": {},
            "callStack": [],
            "memory": [],
            "array": None,
            "arrays": [],
            "explanation": f"❌ {error_msg}",
            "complexity": {
                "opCount": op_count[0],
                "comparisons": 0,
                "swaps": 0,
                "depth": 0
            }
        })

    return {
        "frames": frames,
        "error": error_msg,
        "totalSteps": len(frames)
    }

def generate_trace(code: str, language: str):
    """
    Main entry point for generating traces. Routes to language-specific tracer.
    """
    if language == "python":
        return generate_python_trace(code)
    else:
        return {
            "frames": [],
            "error": f"{language.capitalize()} live tracing is not supported on backend. Please select Python 3.",
            "totalSteps": 0
        }

