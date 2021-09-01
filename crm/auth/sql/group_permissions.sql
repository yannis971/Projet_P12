INSERT INTO auth_group_permissions (group_id, permission_id)
    SELECT 1, permission.id
    FROM auth_permission AS permission
    INNER JOIN django_content_type AS content_type
        ON permission.content_type_id = content_type.id
    WHERE content_type.app_label = 'crm_api'
    AND content_type.model IN ('user', 'salescontact', 'supportcontact', 'staffcontact');

INSERT INTO auth_group_permissions (group_id, permission_id)
    SELECT 1, permission.id
    FROM auth_permission AS permission
    INNER JOIN django_content_type AS content_type
        ON permission.content_type_id = content_type.id
    WHERE content_type.app_label = 'crm_api'
    AND content_type.model IN ('client', 'contract', 'event', 'eventstatus')
    AND (permission.codename like 'change_%' OR permission.codename like 'view_%');

INSERT INTO auth_group_permissions (group_id, permission_id)
    SELECT 2, permission.id
    FROM auth_permission AS permission
    INNER JOIN django_content_type AS content_type
        ON permission.content_type_id = content_type.id
    WHERE content_type.app_label = 'crm_api'
    AND ((content_type.model = 'client' AND (permission.codename like 'add_%' OR permission.codename like 'change_%' OR permission.codename like 'view_%'))
    OR (content_type.model = 'contract' AND (permission.codename like 'add_%' OR permission.codename like 'view_%'))
    OR (content_type.model = 'event' AND (permission.codename like 'add_%' OR permission.codename like 'view_%')));

INSERT INTO auth_group_permissions (group_id, permission_id)
    SELECT 3, permission.id
    FROM auth_permission AS permission
    INNER JOIN django_content_type AS content_type
        ON permission.content_type_id = content_type.id
    WHERE content_type.app_label = 'crm_api'
    AND ((content_type.model = 'client' AND permission.codename like 'view_%')
    OR (content_type.model = 'contract' AND permission.codename = 'change_contract_status')
    OR (content_type.model = 'event' AND (permission.codename like 'change_%' OR permission.codename like 'view_%')));
