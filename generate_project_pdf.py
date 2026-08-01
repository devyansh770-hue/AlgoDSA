import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf():
    pdf_filename = r"c:\Users\Devyansh verma\OneDrive\Desktop\algodsa\AlgoDSA_Project_Documentation.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor('#6366f1')
    secondary_color = colors.HexColor('#0f172a')
    text_dark = colors.HexColor('#1e293b')
    bg_light = colors.HexColor('#f8fafc')
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=body_style,
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderColor=colors.HexColor('#cbd5e1'),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    )

    story = []
    
    # --- HEADER / TITLE ---
    story.append(Paragraph("AlgoDSA Platform — System Architecture & Product Blueprint", title_style))
    story.append(Paragraph("World-Class AI Learning & FAANG Interview Simulator • System Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))

    # --- EXECUTIVE SUMMARY ---
    story.append(Paragraph("1. Executive Summary & Product Vision", h1_style))
    story.append(Paragraph(
        "<b>AlgoDSA is NOT another LeetCode clone or simple Online Judge.</b> Traditional platforms act strictly as code evaluators (submit code &rarr; pass/fail test cases). In contrast, AlgoDSA is an AI-powered learning platform where users learn, think, communicate, and then code.",
        body_style
    ))
    story.append(Paragraph(
        "The core experience revolves around <b>Alex (Google Senior Staff AI Mentor)</b>. In real tech interviews at Google, Meta, or Amazon, coding represents only ~30% of the evaluation. The remaining 70% tests communication, edge-case identification, pattern recognition, and trade-off analysis.",
        body_style
    ))

    # Comparison Table
    table_data = [
        [Paragraph("<b>Feature Component</b>", body_style), Paragraph("<b>Traditional Online Judges (LeetCode/GFG)</b>", body_style), Paragraph("<b>AlgoDSA Platform</b>", body_style)],
        [Paragraph("Core Philosophy", body_style), Paragraph("Passive Code Evaluation & Output Comparison", body_style), Paragraph("Interactive AI FAANG Interview Simulator", body_style)],
        [Paragraph("AI Mentor Integration", body_style), Paragraph("None or static hint text", body_style), Paragraph("Alex — Senior Staff Engineer AI Partner", body_style)],
        [Paragraph("Interview Workflow", body_style), Paragraph("Direct Code Editor access only", body_style), Paragraph("Structured 9-Phase Guided Interview Stepper", body_style)],
        [Paragraph("Multi-Platform Data", body_style), Paragraph("Isolated to single platform", body_style), Paragraph("Unified Aggregator (AlgoDSA + LC + GFG)", body_style)],
        [Paragraph("Retention Tracking", body_style), Paragraph("Simple count of solved questions", body_style), Paragraph("SuperMemo SM-2 Spaced Repetition Engine", body_style)],
    ]
    t = Table(table_data, colWidths=[100, 200, 230])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # --- 9-PHASE INTERVIEW STEPPER ---
    story.append(Paragraph("2. The 9-Phase Google Interview Stepper", h1_style))
    phases = [
        ("Phase 1: Requirements & Constraints", "Clarify problem boundaries, value ranges (e.g. N <= 10^5), and memory constraints."),
        ("Phase 2: Edge Case Analysis", "Identify edge cases (empty inputs, single elements, negative values, duplicates)."),
        ("Phase 3: Pattern Identification", "Select optimal algorithm pattern (Two Pointers, Sliding Window, DP, Trees, Graphs)."),
        ("Phase 4: Approach & Trade-off Analysis", "Discuss Brute Force O(N^2) vs Optimal O(N) space/time trade-offs."),
        ("Phase 5: Communicate Algorithm", "Explain plain-English algorithm to Alex (AI Mentor) before coding."),
        ("Phase 6: Write Code in Monaco Hero Editor", "Write production-grade source code with sub-10ms language conversion."),
        ("Phase 7: Dry Run & Custom Inputs", "Trace code execution line-by-line using custom test suites."),
        ("Phase 8: AI Code & Complexity Review", "Receive 4-part architectural review, time/space complexity O(N), and readiness score."),
        ("Phase 9: Spaced Repetition Scheduling", "Automated SuperMemo SM-2 scheduling for future memory retention."),
    ]
    for p_name, p_desc in phases:
        story.append(Paragraph(f"• <b>{p_name}</b>: {p_desc}", bullet_style))

    story.append(Spacer(1, 8))

    # --- ALEX AI MENTOR ARCHITECTURE ---
    story.append(Paragraph("3. Alex — Google Senior Staff AI Mentor Architecture", h1_style))
    story.append(Paragraph(
        "Alex is implemented as a dedicated service layer in <code>apps/tutor/services/ai.py</code>. Key sub-modules include:",
        body_style
    ))
    story.append(Paragraph("• <b>Progressive 3-Level Nudge Engine</b>: Level 1 (Nudge question) &rarr; Level 2 (Pattern reveal) &rarr; Level 3 (Pseudocode). Never dumps direct code.", bullet_style))
    story.append(Paragraph("• <b>Pre-Code Approach Validator</b>: Warns users if attempting inefficient brute force when optimal pattern exists.", bullet_style))
    story.append(Paragraph("• <b>Socratic Debugging Engine</b>: Asks targeted questions on failed test runs rather than giving answers.", bullet_style))
    story.append(Paragraph("• <b>'Explain It Back' Evaluation</b>: Evaluates user's pattern understanding (Score &ge; 60% unlocks editorial).", bullet_style))
    story.append(Paragraph("• <b>Post-Submission Code Audit</b>: Generates 4-part review (What Went Well, Potential Improvements, FAANG Notes, 4-Metric Scorecard).", bullet_style))

    story.append(Spacer(1, 8))

    # --- MULTI-PLATFORM PROGRESS HUB ---
    story.append(Paragraph("4. Topic Mastery Hub & Single Source of Truth", h1_style))
    story.append(Paragraph("• <b>Strict AlgoDSA Roadmap Progress</b>: Visual progress bar and mastery badges (🌱 Beginner, 🔥 Improving, ⭐ Intermediate, 🏆 Advanced, 👑 Mastered) depend <b>STRICTLY</b> on AlgoDSA curated roadmap completion. External platforms never inflate the denominator.", bullet_style))
    story.append(Paragraph("• <b>Separated Platform Metrics</b>: Each topic header displays <i>AlgoDSA Roadmap Solved</i>, <i>LeetCode Solved</i>, <i>GFG Solved</i>, and <i>Combined Total Unique Solved</i>.", bullet_style))
    story.append(Paragraph("• <b>Multi-Platform Deduplication</b>: Problems solved on multiple platforms (e.g., Two Sum) merge into a single card with checkmark badges (<code>AlgoDSA ✓</code> <code>LeetCode ✓</code> <code>GFG ✓</code>).", bullet_style))
    story.append(Paragraph("• <b>Pagination & Load More</b>: Renders 20 cards initially with a clean <i>Load More (+N remaining)</i> button to handle 100+ solved questions per topic smoothly.", bullet_style))

    story.append(Spacer(1, 8))

    # --- SPACED REPETITION ENGINE ---
    story.append(Paragraph("5. SuperMemo SM-2 Spaced Repetition Engine", h1_style))
    story.append(Paragraph(
        "AlgoDSA implements the SuperMemo SM-2 algorithm in <code>apps/progress/services/spaced_repetition.py</code> to guarantee long-term retention:",
        body_style
    ))
    story.append(Paragraph("I(1) = 1,  I(2) = 6,  I(n) = I(n-1) * EF", code_style))
    story.append(Paragraph(
        "The Easiness Factor (EF) updates dynamically based on review performance (0-5 rating scale). Items due for revision appear automatically in the <b>Review Due</b> tab on the user's workstation.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # --- TECH STACK ---
    story.append(Paragraph("6. Technical Stack & State Isolation Architecture", h1_style))
    story.append(Paragraph("• <b>Backend Engine</b>: Django 5.x, Python 3.12, SQLite / PostgreSQL, RESTful JSON API.", bullet_style))
    story.append(Paragraph("• <b>Frontend Architecture</b>: Vanilla CSS Design System, Alpine.js reactive components, Lucide Icons, Chart.js.", bullet_style))
    story.append(Paragraph("• <b>Monaco Hero Editor</b>: Plain JS <code>MonacoManager</code> closure outside Alpine proxy reactivity to prevent browser freezes; isolated storage keys (<code>algodsa_code_${userId}_${problemId}_${language}</code>); full unescaping pipeline (<code>\\n</code>, <code>\\t</code>, <code>\\\"</code>).", bullet_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=8))
    story.append(Paragraph("Generated by AlgoDSA Platform Documentation Engine • Confidential & Proprietary", ParagraphStyle('FooterText', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#94a3b8'), alignment=1)))

    doc.build(story)
    print("PDF build complete:", pdf_filename)

if __name__ == '__main__':
    build_pdf()
