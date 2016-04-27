from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Util import is_List
import os, struct, subprocess

RESOURCE_ASM_IN = {
    'linux': """
            .section    .rodata
            .global     @name@
            .type       @name@, @object
            .align      4
        @name@:
            .incbin     "@path@"
            .global     @name@_size
            .type       @name@_size, @object
            .align      4
        @name@_size:
            .quad       @name@_size - @name@
    """,

    'mac': """
            .section    __DATA,__const
            .global     _@name@
            .align      4
        _@name@:
            .incbin     "@path@"
            .global     _@name@_size
            .align      4
        _@name@_size:
            .quad       _@name@_size - _@name@
    """,
}

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

    target_dir = os.path.dirname(target[0].abspath)
    encrypted_res_file = os.path.join(target_dir, name + '.encrypted')
    cmd = [
        'openssl',
        'enc',
            '-e',
            '-aes-256-cbc',
            '-k', env['SECRET_KEY'],
            '-in', source_path,
            '-out', encrypted_res_file,
    ]
    subprocess.check_call(cmd)

    with open(encrypted_res_file, 'rb') as f:
        encrypted_data = f.read()
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

def _write_res_asm_in_file(target, source, env):
    with open(target[0].abspath, 'wb') as f:
        f.write(env['__RES_ASM_IN'])

def build_resource_blob(env, source, name='terminus_resources'):
    # Concatenate resources inton a single blob
    blob = env.Command(
        target = name + '.blob',
        source = source,
        action = 'cat $SOURCES > ${TARGET}',
    )

    # Generate pre-substitution assembly file
    env['__RES_ASM_IN'] = RESOURCE_ASM_IN[env['PLATFORM']]
    resource_asm_in = env.Command(
        target = 'resource.s.in',
        source = source,
        action = _write_res_asm_in_file,
    )

    # Perform substitution on pre-substitution assembly file
    env.Tool('textfile')
    subst_dict = {
        '@name@': name,
        '@path@': blob[0].abspath,
    }
    asm_file = env.Substfile(resource_asm_in, SUBST_DICT = subst_dict)

    # Compile assembly file, which will incbin the resource blob
    blob_obj = env.StaticObject(name, asm_file)
    env.Depends(blob_obj, blob)

    return blob_obj

def generate(env):
    env['BUILDERS']['SerializeResource'] = _resource_serializer
    env.AddMethod(build_resource_blob, 'BundleResources')

def exists(env):
    return True
