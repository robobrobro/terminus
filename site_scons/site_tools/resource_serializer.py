from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Defaults import Copy
from SCons.Util import is_List
import binascii, os, struct, subprocess

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

    # Generate IV
    iv = os.urandom(16) # 128 bits (for AES-256)
    iv_size = len(iv)

    target_dir = os.path.dirname(target[0].abspath)
    encrypted_res_file = os.path.join(target_dir, name + '.encrypted')
    cmd = [
        'openssl',
        'enc',
            '-e',
            '-aes-256-cbc',
            '-K', env['SECRET_KEY'],
            '-iv', binascii.hexlify(iv),
            '-nosalt',
            '-in', source_path,
            '-out', encrypted_res_file,
            '-p',
    ]
    subprocess.check_call(cmd)

    with open(encrypted_res_file, 'rb') as f:
        encrypted_data = f.read()
    size = len(encrypted_data)

    # Serialize to target
    # TODO move resource definition to C header
    # Format:
    #   H   size of resource name
    #   s   resource name (# of bytes equal to prev)
    #   H   size of IV
    #   s   IV (# of bytes equal to prev)
    #   Q   size of resource data
    #   s   resource data (# of bytes equal to prev)
    data_format = '<H{}sH{}sQ{}s'.format(name_size, iv_size, size)
    serialized_data = struct.pack(data_format,
        name_size,
        name,
        iv_size,
        iv,
        size,
        encrypted_data
    )
    with open(target[0].abspath, 'wb') as f:
        f.write(serialized_data)

_resource_serializer = Builder(
    action = Action(serialize_resource, 'Serializing resource $SOURCE -> $TARGET'),
    suffix = '.res',
)

def build_resource_blob(env, source, name='terminus_resources'):
    # Concatenate resources inton a single blob
    blob = env.Command(
        target = name + '.blob',
        source = source,
        action = 'cat $SOURCES > ${TARGET}',
    )

    # Copy pre-substitution assembly file to build directory
    pre_subst_asm_file = env.Command(
        target = name + '.S.in',
        source = '#asm/$OS/resource.S.in',
        action = Copy('$TARGET', '$SOURCE'),
    )

    # Perform substitution on pre-substitution assembly file
    env.Tool('textfile')
    subst_dict = {
        '@name@': name,
        '@path@': blob[0].abspath,
    }
    asm_file = env.Substfile(pre_subst_asm_file, SUBST_DICT = subst_dict)

    # Compile assembly file, which will incbin the resource blob
    blob_obj = env.Command(
        target = name,
        source = asm_file,
        action = '$AS $ASFLAGS -o $TARGET $SOURCE',
    )
    env.Depends(blob_obj, blob)

    return blob_obj

def generate(env):
    env['BUILDERS']['SerializeResource'] = _resource_serializer
    env.AddMethod(build_resource_blob, 'BundleResources')

def exists(env):
    return True
