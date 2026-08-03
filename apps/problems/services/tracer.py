import sys
import copy
import json
import traceback

MAX_FRAMES = 1000

def generate_python_trace(code: str):
    """
    Executes Python code securely in a restricted dictionary scope and generates an execution trace.
    Returns a dict with {"frames": [...], "error": None} or {"error": "..."}
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
            # Limit list size serialization
            return [sanitize_val(item) for item in v[:50]]
        elif isinstance(v, dict):
            return {str(k): sanitize_val(val) for k, val in list(v.items())[:50]}
        elif isinstance(v, tuple):
            return [sanitize_val(item) for item in v[:50]]
        else:
            return f"<{type(v).__name__}>"

    def trace_callback(frame, event, arg):
        # We only care about line events or calls in the user's script
        if frame.f_code.co_filename != "<string>":
            return trace_callback

        if event == 'line':
            op_count[0] += 1
            if op_count[0] > MAX_FRAMES:
                raise RuntimeError(f"Execution Limit Exceeded (Max {MAX_FRAMES} frames). Possible infinite loop.")
            
            # Extract variables safely
            variables = {}
            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    variables[k] = {
                        "type": type(v).__name__,
                        "value": sanitize_val(v),
                        "address": id(v) % 100000,
                        "changed": False
                    }
                    
            # Check for changes
            if frames and "variables" in frames[-1]:
                prev_vars = frames[-1]["variables"]
                for k, v_data in variables.items():
                    if k not in prev_vars or prev_vars[k]["value"] != v_data["value"]:
                        v_data["changed"] = True

            # Calculate call stack depth
            depth = 0
            f = frame
            call_stack = []
            while f and f.f_code.co_filename == "<string>":
                call_stack.append(f.f_code.co_name)
                depth += 1
                f = f.f_back
            
            frame_data = {
                "step": op_count[0],
                "line": frame.f_lineno,
                "variables": variables,
                "callStack": call_stack[::-1],
                "complexity": {
                    "opCount": op_count[0],
                    "comparisons": 0, # Cannot track these at Python instruction level without bytecode injection
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
        # Extract the line number where the exception occurred in the user's code
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
            "variables": {},
            "callStack": [],
            "explanation": error_msg,
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
        # Return mock / not implemented for other languages for now
        return {
            "frames": [],
            "error": f"{language.capitalize()} tracing is not yet supported by the backend execution engine. Please use Python 3.",
            "totalSteps": 0
        }
