def build_and_compress(env, source, target):
    env.Tool('compactor')
    uncompressed = env.Program('uncompressed', source)
    compressed = env.Compact(
        target = target,
        source = uncompressed,
    )
    return compressed

def generate(env):
    env.AddMethod(build_and_compress, 'BuildAndCompress')

def exists(env):
    return True
