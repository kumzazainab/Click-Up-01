import pytz

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('project manager', 'Project Manager'),
    ('employee', 'Employee'),
)


STATUS = (
    ('todo', 'To Do'),
    ('in_progress', 'In Progress'),
    ('in_review', 'In Review'),
    ('need_to_discuss', 'Need to Discuss'),
    ('reopen', 'Reopen'),
    ('waiting_to_be_merged', 'Waiting to be Merged'),
    ('complete', 'Complete'),
)

STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('started', 'Started'),
        ('finished', 'Finished'),
)

APPEARANCE_CHOICES = (
    ('light', 'Light'),
    ('dark', 'Dark'),
    ('auto', 'Auto'),
)

TWO_FACTOR_CHOICES = (
    ('none', 'None'),
    ('sms', 'SMS'),
    ('totp', 'Authenticator App'),
)

LanguageSelector = (
    ('english', 'English'),
    ('french', 'French'),
    ('espanol', 'Espanol'),
    ('portuguese(brasil)', 'Portuguese(Brasil)'),
    ('deutsch', 'Deutsch'),
    ('italiano', 'Italiano'),
)

THEME_COLORS = (
    ('green', 'Green'),
    ('plum', 'Plum'),
    ('purple', 'Purple'),
    ('lightblue', 'Light Blue'),
    ('oat', 'Oat'),
    ('pink', 'Pink'),
    ('cyan', 'Cyan'),
    ('grey', 'Grey'),
    ('cadmium orange', 'Cadmium Orange'),
)

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

WORKSPACE_TYPES = (
    ('work', 'Work'),
    ('personal', 'Personal'),
    ('school', 'School'),
)

MANAGE_TYPES = (
    ('hr_recruiting', 'HR & Recruiting'),
    ('marketing', 'Marketing'),
    ('it', 'IT'),
    ('personal_use', 'Personal Use'),
    ('pmo', 'PMO'),
    ('professional_services', 'Professional Services'),
    ('software_development', 'Software Development'),
    ('support', 'Support'),
    ('startup', 'Startup'),
    ('operations', 'Operations'),
    ('sales_crm', 'Sales & CRM'),
    ('others', 'Others'),
)

TOOLS_CHOICES = (
    ('dropbox', 'Dropbox'),
    ('monday', 'Monday'),
    ('basecamp', 'Basecamp'),
    ('salesforce', 'Salesforce'),
    ('trello', 'Trello'),
    ('todolist', 'Todoist'),
    ('jira', 'Jira'),
    ('gdrive', 'Google Drive'),
    ('figma', 'Figma'),
    ('github', 'GitHub'),
    ('slack', 'Slack'),
    ('ms_teams', 'MS Teams'),
    ('excel_csv', 'Excel & CSV'),
    ('asana', 'Asana'),
)

FEATURES_CHOICES = (
    ('docs_wikis', 'Docs & Wikis'),
    ('sprints', 'Sprints'),
    ('calendar', 'Calendar'),
    ('goals_okrs', 'Goals & OKRs'),
    ('clips', 'Clips'),
    ('boards', 'Boards'),
    ('dashboard', 'Dashboard'),
    ('chat', 'Chat'),
    ('time_tracking', 'Time Tracking'),
    ('crm', 'CRM'),
    ('automations', 'Automations'),
    ('ask_ai', 'Ask AI'),
    ('scheduling', 'Scheduling'),
    ('tasks_projects', 'Tasks & Projects'),
    ('whiteboards', 'Whiteboards'),
)

RESOURCE_CHOICES = (
    ('linkedin', 'LinkedIn'),
    ('tv', 'TV'),
    ('youtube', 'YouTube'),
    ('google', 'Google'),
    ('facebook', 'Facebook'),
    ('friends/colleagues', 'Friends & Colleagues'),
    ('reddit', 'Reddit'),
    ('instagram', 'Instagram'),
    ('tiktok', 'TikTok'),
    ('software review site', 'Software Review site'),
    ('search engines(google, bing)', 'Search Engines (Google, bing)'),
    ('others', 'Others'),
)
