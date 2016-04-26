from __future__ import print_function
from cryptography.fernet import Fernet
from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Util import is_List
import os
import struct

def serialize_resource(target, source, env):
    # Convert source to a list of SCons Files
    if not is_List(source):
        source = [env.File(source).srcnode()]

    # Determine name of resource
    source_path = source[0].abspath
    name = os.path.splitext(os.path.basename(source_path))[0]
    name_size = len(name)

    # Encrypt resource data
    with open(source_path, 'rb') as f:
        data = f.read()

    fern = Fernet(env['SECRET_KEY'])
    print ('Encrypting with key: {}'.format(env['SECRET_KEY']))
    encrypted_data = fern.encrypt(data)
    size = len(encrypted_data)

    # Serialize to target
    data_format = '<H{}sQ{}s'.format(name_size, size)
    serialized_data = struct.pack(data_format, name_size, name, size, encrypted_data)
    with open(target[0].abspath, 'wb') as f:
        f.write(serialized_data)

_resource_serializer = Builder(
    action = Action(serialize_resource, 'Serializing resource $SOURCE -> $TARGET'),
    suffix = '.res',
)

def generate(env):
    env['BUILDERS']['SerializeResource'] = _resource_serializer

def exists(env):
    return True
