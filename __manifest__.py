# Copyright 2017-2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Soko Fresh Farmer Engagement",
    "summary": "Farmer Registration, Agent Registration, Harvesters Registration",
    "version": "13.0.1.3.0",
    "license": "LGPL-3",
    "website": "https://sokofresh.com",
    "author": "Peter Mudoko",
    "category": "Finance ",
    "depends": ["base", "sales_team","hr"],
    "data": [

        "views/farmer_registration.xml",
        "views/res_partner_county.xml",
        "security/farmer_engagement_security.xml",
        "security/ir.model.access.csv",
       "data/farmer_registration_seq.xml",

    ],
    'images': ['static/description/banner.png'],
    "installable": True,
}
