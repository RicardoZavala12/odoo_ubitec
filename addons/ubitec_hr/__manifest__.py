# -*- coding: utf-8 -*-
{
    "name": "Ubitec - Personal",
    "summary": "Puestos, vacaciones y permisos del personal de Ubitec.",
    "version": "18.0.1.1.0",
    "category": "Human Resources",
    "author": "Ubitec",
    "license": "LGPL-3",
    "depends": ["hr", "hr_holidays", "gps_service"],
    "data": [
        "data/hr_job_data.xml",
        "data/mandatory_days_data.xml",
        "data/accrual_plan_data.xml",
        "views/gps_service_views.xml",
    ],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
}
