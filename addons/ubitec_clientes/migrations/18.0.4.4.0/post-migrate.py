import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    def grp(xmlid):
        return env.ref(xmlid, raise_if_not_found=False)

    def restringir_menu(xmlid_menu, grupos):
        menu = env.ref(xmlid_menu, raise_if_not_found=False)
        ids = [g.id for g in grupos if g]
        if menu and ids:
            menu.write({"groups_id": [(6, 0, ids)]})

    def limpiar_extra(usuario, xmlids_a_quitar):
        if not usuario:
            return
        quitar = [(3, g.id) for g in (grp(x) for x in xmlids_a_quitar) if g]
        if quitar:
            usuario.write({"groups_id": quitar})

    comercial = grp("ubitec_clientes.group_ubitec_comercial")
    ventas_user = grp("sales_team.group_sale_salesman")
    invoicing = grp("account.group_account_invoice")
    gps_scheduler = grp("gps_service.group_gps_scheduler")
    admin_settings = grp("base.group_system")
    hr_officer = grp("hr.group_hr_user")
    hr_manager = grp("hr.group_hr_manager")
    holidays_manager = grp("hr_holidays.group_hr_holidays_manager")

    # ── 1) Asignar grupos correctos a cada usuario real ──
    ventas = env["res.users"].search([("login", "=", "ventas@ubitec.mx")], limit=1)
    soporte = env["res.users"].search([("login", "=", "soporte@ubitec.mx")], limit=1)
    admin_ubitec = env["res.users"].search([("login", "=", "admin.ubitec@ubitec.mx")], limit=1)
    tecnico = env["res.users"].search([("login", "=", "tecnico@ubitec.mx")], limit=1)
    tecnico_nuevo = env["res.users"].search([("login", "=", "tecnico@ubitecgps.com")], limit=1)

    # Usuario creado a mano con un monton de permisos de mas (Administrador
    # de Ventas, RH, Flotilla, Contabilidad, etc). Se reemplaza su lista de
    # grupos por completo: solo Interno + Tecnico, igual que el otro tecnico.
    base_user = grp("base.group_user")
    gps_tecnico = grp("gps_service.group_gps_technician")
    if tecnico_nuevo and base_user and gps_tecnico:
        tecnico_nuevo.write({"groups_id": [(6, 0, [base_user.id, gps_tecnico.id])]})

    if ventas:
        nuevos = [g.id for g in (comercial, ventas_user, invoicing) if g]
        ventas.write({"groups_id": [(4, gid) for gid in nuevos]})

    if soporte:
        nuevos = [g.id for g in (comercial, ventas_user, gps_scheduler) if g]
        soporte.write({"groups_id": [(4, gid) for gid in nuevos]})

    if admin_ubitec and comercial:
        admin_ubitec.write({"groups_id": [(4, comercial.id)]})

    # Grupos sueltos que quedaron de pruebas anteriores y abren modulos de
    # mas (Inventario, Asistencias, Empleados): cada usuario se limpia solo
    # a lo que su rol realmente necesita. "Technical Features" no se puede
    # quitar por usuario porque "Internal User" lo implica automaticamente
    # en esta instalacion -> el menu que lo usa se restringe aparte abajo.
    limpiar_extra(tecnico, [
        "stock.group_stock_user",
        "hr_attendance.group_hr_attendance_own_reader",
    ])
    limpiar_extra(soporte, [
        "hr.group_hr_user",
    ])
    limpiar_extra(ventas, [
        "hr_attendance.group_hr_attendance_own_reader",
    ])

    # ── 2) Restringir menus raiz que no tenian ningun grupo asignado ──
    if comercial:
        restringir_menu("ubitec_clientes.menu_ubitec_root", [comercial])
        restringir_menu("contacts.menu_contacts", [comercial])
    if ventas_user:
        restringir_menu("sale.sale_menu_root", [ventas_user])
    if admin_settings:
        restringir_menu("base.menu_management", [admin_settings])
        restringir_menu("base.menu_tests", [admin_settings])
        restringir_menu("project_todo.menu_todo_todos", [admin_settings])
        restringir_menu("utm.menu_link_tracker_root", [admin_settings])

    # ── 3) Empleados/Vacaciones: quitar "Usuario interno" como llave,
    #      solo admins/officers de RH (nadie pidio que operativos lo vean) ──
    if hr_officer and hr_manager:
        restringir_menu("hr.menu_hr_root", [hr_officer, hr_manager])
    if holidays_manager:
        restringir_menu("hr_holidays.menu_hr_holidays_root", [holidays_manager])
