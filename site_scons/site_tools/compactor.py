from SCons.Builder import Builder

_builder = Builder(
    action = 'upx -9 -o $TARGET $SOURCES',
)

def generate(env):
    env['BUILDERS']['Compact'] = _builder

def exists(env):
    return True
