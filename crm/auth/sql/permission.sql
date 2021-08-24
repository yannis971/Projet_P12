INSERT INTO auth_permission (name, content_type_id, codename)
    SELECT 'Can change contract status', content_type.id, 'change_contract_status'
        FROM django_content_type as content_type
        WHERE content_type.app_label = 'crm_api' and content_type.model = 'contract';
