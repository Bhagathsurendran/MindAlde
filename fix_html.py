import os
import re

directories = ['templates', 'routes', '.']

replacements = {
    r"url_for\(['\"]login['\"]\)": "url_for('auth.login')",
    r"url_for\(['\"]register['\"]\)": "url_for('auth.register')",
    r"url_for\(['\"]dashboard['\"]\)": "url_for('auth.dashboard')",
    r"url_for\(['\"]admin_dashboard['\"]\)": "url_for('auth.admin_dashboard')",
    r"url_for\(['\"]caretaker_dashboard['\"]\)": "url_for('auth.caretaker_dashboard')",
    r"url_for\(['\"]patient_dashboard['\"]\)": "url_for('auth.patient_dashboard')",
    r"url_for\(['\"]manage_users['\"]\)": "url_for('auth.manage_users')",
    r"url_for\(['\"]edit_user['\"]": "url_for('auth.edit_user'",
    r"url_for\(['\"]delete_user['\"]": "url_for('auth.delete_user'",
    
    r"url_for\(['\"]manage_quiz['\"]\)": "url_for('quiz.manage_quiz')",
    r"url_for\(['\"]edit_quiz['\"]": "url_for('quiz.edit_quiz'",
    r"url_for\(['\"]delete_quiz['\"]": "url_for('quiz.delete_quiz'",
    
    r"url_for\(['\"]therapist_dashboard['\"]\)": "url_for('therapists.therapist_dashboard')",
    r"url_for\(['\"]manage_therapists['\"]\)": "url_for('therapists.manage_therapists')",
    r"url_for\(['\"]verify_therapist['\"]": "url_for('therapists.verify_therapist'",
    r"url_for\(['\"]reject_therapist['\"]": "url_for('therapists.reject_therapist'",
    r"url_for\(['\"]edit_therapist['\"]": "url_for('therapists.edit_therapist'",
    r"url_for\(['\"]delete_therapist['\"]": "url_for('therapists.delete_therapist'",
    r"url_for\(['\"]therapist_suggestions['\"]\)": "url_for('auth.therapist_suggestions')",
}

for d in directories:
    if not os.path.isdir(d):
        continue
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.html') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                if file == "fix_html.py":
                    continue
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for pattern, replace in replacements.items():
                    new_content = re.sub(pattern, replace, new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")
