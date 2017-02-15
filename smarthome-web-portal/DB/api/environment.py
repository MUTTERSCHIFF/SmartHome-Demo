# -*- coding: utf-8 -*-
"""
CRUD operation for environment model
"""
from DB.api import database
from DB import exception
from DB.models import Environment
from DB.api import dbutils as utils


RESP_FIELDS = ['id', 'uuid', 'gateway_id', 'temperature', 'humidity', 'pressure', 'uv_index', 'created_at']
SRC_EXISTED_FIELD = {'id': 'id',
                     'uuid': 'uuid',
                     'temperature': 'temperature',
                     'humidity': 'humidity',
                     'pressure': 'pressure',
                     'uv_index': 'uv_index',
                     'gateway_id': 'gateway_id',
                     'created_at': 'created_at'
                     }


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)
def new(session, src_dic, content={}):
    for k, v in SRC_EXISTED_FIELD.items():
        content[k] = src_dic.get(v, None)
    return utils.add_db_object(session, Environment, **content)


def _get_env(session, gateway_id, uuid, order_by=[], limit=None, **kwargs):
    if isinstance(uuid, basestring):
        ids = {'eq': uuid}
    elif isinstance(uuid, list):
        ids = {'in': uuid}
    else:
        raise exception.InvalidParameter('parameter uuid format are not supported.')
    return \
        utils.list_db_objects(session, Environment, order_by=order_by, limit=limit,
                              gateway_id=gateway_id, uuid=ids, **kwargs)


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_env_by_gateway_uuid(session, gateway_id, uuid):
    return _get_env(session, gateway_id, uuid)


# get the latest data if exists
@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)      # wrap the raw DB object into dict
def get_latest_by_gateway_uuid(session, gateway_id, uuid, ):
    env = _get_env(session, gateway_id, uuid, order_by=[('id', True)], limit=1)
    return env[0] if len(env) else None
