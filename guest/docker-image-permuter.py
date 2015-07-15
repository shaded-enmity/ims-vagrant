#!/usr/bin/python -tt

import os, sys, subprocess, random, re, tempfile

BASE_IMAGES = ['fedora:21', 'fedora:22', 'busybox:latest']
LABELS_TLDS = ['acme', 'isv', 'corp']

DOCKERFILE_TEMPLATE = '''FROM {0}
LABEL {1}
{2}
CMD ["echo", "test image"]'''

WORDS = open('/usr/share/dict/words').readlines()

def generate_version():
        return '{0}.{1}.{2}-{3}'.format(*map(lambda x: x(1, 20), [random.randrange]*4))

def generate_word():
        n = random.choice(WORDS)
        if len(n) < 3:
                return generate_word()
        return re.sub(r'\W+', '', n.strip())

def generate_value():
        n = random.randrange(3)
        if n == 0:
                return hex(random.randrange(0, 2**32))
        elif n == 1:
                return random.choice(['true', 'false', '0', '1'])
        else:
                return generate_word()

def generate_content(file_path):
        return 'dd if=/dev/urandom of={0} bs=4096 count=1'.format(file_path)

def generate_label(tld):
        return '{0}.{1}="{2}"'.format(tld, generate_word(), generate_value())

def random_dockerfile():
        from_K = random.choice(BASE_IMAGES)
        label_TLD = random.choice(LABELS_TLDS)
        numlabels = random.randrange(1, 5)
        version = generate_version()
        label_K = map(generate_label, [label_TLD]*numlabels) + ['version="' + version + '"'] + ['base_image="' + from_K + '"']
        layers = [1] * random.randrange(1, 4)

        return (version, DOCKERFILE_TEMPLATE.format(
                from_K,
                ' '.join(label_K),
                '\n'.join(['RUN ' + generate_content('/content') for l in layers])
        ))

def create_image(registry_url, repo):
        ver, df = random_dockerfile()
        ctx = tempfile.mkdtemp()

        with open(os.path.join(ctx, 'Dockerfile'), 'a+') as f:
                f.write(df)
        
        print '{0}/{1}:{2}'.format(registry_url, repo, ver)
        return subprocess.check_output([
                'docker',
                'build',
                '--rm',
                '-t',
                '{0}/{1}:{2}'.format(registry_url, repo, ver),
                ctx
        ])

def create_repo(name, registry_url, numx=2):
        numimgs = random.randrange(1, numx)
        for i in range(numimgs):
                create_image(registry_url, name)

repo = generate_word() + '/' + generate_word()
repo = repo.lower()
create_repo(repo, sys.argv[1])
