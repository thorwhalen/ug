"""Utils for ug"""

import os
from typing import Union, Any, MutableMapping, Callable, KT, VT

from googlemaps import Client

DFLT_GOOGLE_API_KEY_ENV_VAR = '$GOOGLE_API_KEY'


APIKeyT = str
EnvVarT = str
ClientSpec = Union[APIKeyT, EnvVarT, Client, None]
KvWriterFunc = Callable[[KT, Any], None]
KvWriterSpec = Union[MutableMapping, KvWriterFunc]


def resolve_env_var_if_starts_with_dollar_sign(x: Any) -> bool:
    if isinstance(x, str) and x.startswith('$'):
        return os.environ.get(x[1:])
    else:
        return x


def ensure_gmaps_client(
    client_spec: ClientSpec = DFLT_GOOGLE_API_KEY_ENV_VAR,
) -> Client:
    if isinstance(client_spec, Client):
        # if client_spec is already a Client object, just return it
        return client_spec
    else:
        key = resolve_env_var_if_starts_with_dollar_sign(client_spec)
        # at this point key could be None, or the actual key itself...
        return Client(key=key)


def ensure_kv_writer(writer_spec: KvWriterSpec) -> KvWriterFunc:
    if callable(writer_spec):
        return writer_spec
    else:
        return writer_spec.__setitem__
