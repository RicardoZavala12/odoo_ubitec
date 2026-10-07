# -*- coding: utf-8 -*-
import logging
import secrets


_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Assign initial jobs and create the root account once, using the ORM."""
    leave_type = env.ref("hr_holidays.holiday_status_cl", raise_if_not_found=False)
    if leave_type:
        leave_type.write({"name": "Vacaciones"})

    employee_jobs = {
        "Oscar": "job_tecnico_instalacion",
        "Magali": "job_soporte_agenda",
        "Administrator": "job_administrativo",
        "Reyna": "job_administrativo",
        "Carlos": "job_administrativo",
        "Adrian": "job_administrativo",
        "Israel": "job_administrativo",
        "Paola": "job_administrativo",
        "Eliud": "job_administrativo",
        "Aaron": "job_administrativo",
        "Roberto": "job_administrativo",
        "Liliana": "job_administrativo",
        "Jorge": "job_administrativo",
        "Ileana": "job_administrativo",
    }
    for employee_name, job_xml_id in employee_jobs.items():
        employee = env["hr.employee"].search(
            [("name", "=", employee_name)], limit=1
        )
        if employee:
            employee.write({"job_id": env.ref("ubitec_hr." + job_xml_id).id})

    employee_logins = {
        "Oscar": "tecnico@ubitec.mx",
        "Magali": "soporte@ubitec.mx",
    }
    for employee_name, login in employee_logins.items():
        employee = env["hr.employee"].search([("name", "=", employee_name)], limit=1)
        user = env["res.users"].sudo().search([("login", "=", login)], limit=1)
        if employee and user and not employee.user_id:
            employee.write({"user_id": user.id})

    users = env["res.users"].sudo()
    if users.search([("login", "=", "root@ubitec.mx")], limit=1):
        return

    admin_ubitec = users.search(
        [("login", "=", "admin.ubitec@ubitec.mx")], limit=1
    )
    generated_password = secrets.token_urlsafe(12)
    values = {
        "name": "Ricky (Root)",
        "login": "root@ubitec.mx",
        "email": "root@ubitec.mx",
        "password": generated_password,
    }
    if admin_ubitec:
        values["groups_id"] = [(6, 0, admin_ubitec.groups_id.ids)]
    users.create(values)

    # Emit the generated credential only on creation, for the installation operator.
    _logger.info(
        "UBITEC: created root@ubitec.mx; admin.ubitec@ubitec.mx found: %s; "
        "generated password: %s",
        bool(admin_ubitec),
        generated_password,
    )
    if not admin_ubitec:
        _logger.warning(
            "UBITEC: admin.ubitec@ubitec.mx was not found; root@ubitec.mx "
            "was created with Odoo default groups. Review its access manually."
        )
