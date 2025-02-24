from .common import (
    start,
    help_,
    is_sending_to_admin,
    accept,

)
from .common_text import (
    main_menu
)
from .common_docx import (
    documents_main_menu
)
from .admin.admin import (
    add_button,
    admin_menu,
    select_buttongroup_in_create_group,
    save_button_to_file,
    list_buttons,
    delete_button_from_file,
    button_actions,
    edit_button_callback_name,
    edit_button_menu,
    button_group_actions,
    select_button_group,
    delete_group_from_file,
    list_button_group,
    cancellation_button,
    create_button_group,
    select_txt_or_docx_in_view_button_group,
    analyze_and_fill_common_admin,
    analyze_and_fill_common_admin_docx,
    view_all_buttons_in_button_group,
    texts_admin_menu,
    documents_admin_menu,
    button_admin_menu,
    admin_menu_call,
    view_button_group_in_select_txt,
    view_button_group_in_select_docx,
    edit_group,
    edit_group_name,
    get_is_document_group,
    select_buttongroup_in_create_button
)



from .admin.save_doc import (
    change_documents,
    choose_move,
    changing,
    create_document,
    add_new_document,

)