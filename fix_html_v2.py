import os, re

files_with_issues = {}
for d in ['templates', 'routes']:
    if not os.path.isdir(d): continue
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.html') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = re.findall(r"url_for\(['\"]([^.]+?)['\"]", content)
                for m in matches:
                    if m != 'static':
                        if m not in files_with_issues:
                            files_with_issues[m] = []
                        files_with_issues[m].append(filepath)

replacements = {
    'logout': 'auth.logout',
    'selfcare_suggestions': 'selfcare.selfcare_home',
    'caretaker_therapist_suggestions': 'therapists.view_therapists',
    'quiz_page': 'quiz.quiz_page',
    'update_therapist': 'therapists.edit_therapist',
    'add_quiz': 'quiz.manage_quiz',
    'add_therapist': 'therapists.manage_therapists',
    'verify_therapist_account': 'therapists.verify_therapist',
    'reject_therapist_account': 'therapists.reject_therapist',
    'submit_quiz': 'quiz.quiz_page',
    'home': 'auth.home',
    'accept_appointment': 'therapists.accept_appointment',
    'reject_appointment': 'therapists.reject_appointment',
    'request_appointment': 'therapists.request_appointment'
}

for m, files in files_with_issues.items():
    if m in replacements:
        for f in files:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            new_content = re.sub(r"url_for\(['\"]" + m + r"['\"]\)", f"url_for('{replacements[m]}')", content)
            if new_content != content:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated {f}")
