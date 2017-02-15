# -*- coding: utf-8 -*-
"""
CRUD operation for button model
"""
from DB.api import database
from DB import exception
from DB.models import Button
from DB.api import dbutils as utils


RESP_FIELDS = ['id', 'status', 'resource', 'created_at']
SRC_EXISTED_FIELD = {
    'id': 'id',
    # 'uuid': 'uuid',
    'status': 'status',
    'resource_id': 'resource_id',
    'created_at': 'created_at'
}


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)
def new(session, src_dic, content={}):
    for k, v in SRC_EXISTED_FIELD.items():
        content[k] = src_dic.get(v, None)
    return utils.add_db_object(session, Button, **content)


def _get_button(session, resource_id, order_by=[], limit=None, **kwargs):
    if isinstance(resource_id, int):
        resource_ids = {'eq': resource_id}
    elif isinstance(resource_id, list):
        resource_ids = {'in': resource_id}
    else:
        raise exception.InvalidParameter('parameter uuid format are not supported.')
    return \
        utils.list_db_objects(session, Button, order_by, limit=limit, resource_id=resource_ids, **kwargs)


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_button_by_gateway_uuid(session, resource_id):
    return _get_button(session, resource_id)


# get the latest true status if exists
@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)      # wrap the raw DB object into dict
def get_latest_alert_by_gateway_uuid(session, resource_id, token):
    date_range = {'gt': token}
    button = _get_button(session, resource_id, order_by=[('id', True)], limit=1,
                         status=True, created_at=date_range)
    # get latest status
    now = _get_button(session, resource_id, order_by=[('id', True)], limit=1)
    latest = now[0] if len(now) else None
    latest_status = latest.status if latest else None
    # print "latest: " + str(latest_status) + ' button: ' + str(len(button))
    return button[0] if latest_status and len(button) else None


# get the latest status if exists
@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)      # wrap the raw DB object into dict
def get_latest_by_gateway_uuid(session, resource_id, ):
    button = _get_button(session, resource_id, order_by=[('id', True)], limit=1)
    return button[0] if len(button) else None


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_button_by_time(session, start_time, end_time):
    return utils.list_db_objects(session, Button, created_at={'ge': str(start_time), 'le': str(end_time)})\

