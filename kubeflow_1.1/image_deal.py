# -*- coding: utf-8 -*-

import os
import signal

from tqdm import tqdm
from multiprocessing import cpu_count, Pool

git_base_path = '../../gcr.io-images/kubeflow1.1'
image_base = './images_list'

docker_commond_path = './kubeflow_1.1_images_cmd'

docker_gcr_commond_path = './kubeflow_1.1_images_gcr_cmd'

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def multi_process_map_async(func, items):
    pool = Pool(processes=cpu_count() - 2, initializer=init_worker, maxtasksperchild=400)
    ret = pool.map_async(func, items)
    pool.close()
    pool.join()
    # return ret.get() if ret.successful() else []


lines = None
with open(image_base, 'r') as f:
    lines = f.readlines()


docker_gcr_pull_cmd_arr = []
docker_gcr_tag_cmd_arr = []
docker_gcr_push_cmd_arr = []

docker_pull_cmd_arr = []
docker_tag_cmd_arr = []
docker_push_cmd_arr = []

docker_hub_tag_cmd_arr = []
docker_hub_push_cmd_arr = []

sed_cmd_arr = []

line_clean_arr = []

system_cmd_exec_arr = []

for line in lines:

    if line is None or '' == line or '\n' == line:
        continue

    line = line.replace('\n', '')

    if line in line_clean_arr:
        continue

    line_clean_arr.append(line)

    arr = line.split(':')

    old_name = arr[0]
    old_version = arr[1]
    
    name = old_name
    version = old_version
    
    if '@sha256' in line:
        name = name.replace('@sha256', '')
        version = 'lastest'

    print(name + ':' + version)

    simple_name = name.replace('gcr.io/', '')

    # 创建git目录
    git_path = '%s/%s' % (git_base_path, simple_name)
    if not os.path.exists(git_path):
        os.makedirs(git_path)

    # dockerfile
    dockerfile_path = '%s/Dockerfile' % git_path

    if not os.path.exists(dockerfile_path):
        dockerfile_content = "FROM %s" % line

        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)

    image_name = simple_name.replace('/', '.')
    docker_image_name = 'docker.io/chongchuanbing/%s:%s' % (image_name, version)

    # docker pull
    docker_pull_cmd = 'docker pull %s' % docker_image_name
    docker_pull_cmd_arr.append(docker_pull_cmd)
    docker_pull_cmd_arr.append('\n')
    print(docker_pull_cmd)

    # docker tag
    new_tag = 'harbor.ihomefnt.com/ai/%s:%s' % (image_name, version)
    docker_tag_cmd = 'docker tag %s %s' % (docker_image_name, new_tag)
    docker_tag_cmd_arr.append(docker_tag_cmd)
    docker_tag_cmd_arr.append('\n')
    print(docker_tag_cmd)

    # docker push
    docker_push_cmd = 'docker push %s' % new_tag
    docker_push_cmd_arr.append(docker_push_cmd)
    docker_push_cmd_arr.append('\n')
    print(docker_push_cmd)

    print('\n')

    # docker gcr pull
    docker_gcr_pull_cmd = 'docker pull %s' % line
    docker_gcr_pull_cmd_arr.append(docker_gcr_pull_cmd)
    docker_gcr_pull_cmd_arr.append('\n')
    print(docker_gcr_pull_cmd)

    # docker gcr tag
    new_tag = 'harbor.ihomefnt.com/ai/%s:%s' % (image_name, version)
    docker_gcr_tag_cmd = 'docker tag %s %s' % (line, new_tag)
    docker_gcr_tag_cmd_arr.append(docker_gcr_tag_cmd)
    docker_gcr_tag_cmd_arr.append('\n')
    print(docker_gcr_tag_cmd)

    # docker gcr push
    docker_gcr_push_cmd = 'docker push %s' % new_tag
    docker_gcr_push_cmd_arr.append(docker_gcr_push_cmd)
    docker_gcr_push_cmd_arr.append('\n')
    print(docker_gcr_push_cmd)

    # docker hub tag
    hub_new_tag = 'docker.io/chongchuanbing/%s:%s' % (image_name, version)
    docker_hub_tag_cmd = 'docker tag %s %s' % (line, hub_new_tag)
    docker_hub_tag_cmd_arr.append(docker_hub_tag_cmd)
    docker_hub_tag_cmd_arr.append('\n')
    print(docker_hub_tag_cmd)

    # docker hub push
    docker_hub_push_cmd = 'docker push %s' % hub_new_tag
    docker_hub_push_cmd_arr.append(docker_hub_push_cmd)
    docker_hub_push_cmd_arr.append('\n')
    print(docker_hub_push_cmd)

    if '@sha256' in line:
        sed_cmd_special = 'grep -rl "%s" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?%s?%s:%s?"' % (line, line, sed_image, version)
        sed_cmd_arr.append(sed_cmd_special)
        sed_cmd_arr.append('\n')

    sed_image = 'harbor.ihomefnt.com/ai/%s' % image_name
    sed_image = hub_new_tag
    sed_cmd = 'grep -rl "%s" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?%s?%s?"' % (name, name, sed_image)
    sed_cmd_arr.append(sed_cmd)
    
    sed_cmd_arr.append('\n')
    print(sed_cmd)

    arr = []
#     arr.append(docker_gcr_pull_cmd)
#     arr.append(docker_gcr_tag_cmd)

#     arr.append(docker_gcr_push_cmd)
    if '@sha256' in line:
        arr.append(sed_cmd_special)    
    arr.append(sed_cmd)
    
#     arr.append(docker_hub_tag_cmd)
#     arr.append(docker_hub_push_cmd)

    system_cmd_exec_arr.append(arr)


with open(docker_commond_path, 'w') as f:
    f.writelines(docker_pull_cmd_arr)
    f.write('\n')
    f.writelines(docker_tag_cmd_arr)
    f.write('\n')
    f.writelines(docker_push_cmd_arr)
    f.write('\n')
    f.writelines(sed_cmd_arr)


with open(docker_gcr_commond_path, 'w') as f:
    f.writelines(docker_gcr_pull_cmd_arr)
    f.write('\n')
    f.writelines(docker_gcr_tag_cmd_arr)
    f.write('\n')
    f.writelines(docker_gcr_push_cmd_arr)
    f.write('\n')
    f.write('\n')
    f.writelines(docker_hub_tag_cmd_arr)
    f.write('\n')
    f.writelines(docker_hub_push_cmd_arr)
    f.write('\n')

def cmd_deal(system_cmd_exec_arr):
    try:
        for item in system_cmd_exec_arr:
            print('========', item)
            with os.popen(item) as f:
                print(f.read())
    except Exception as error:
        # logger.error(error)
        # logger.error(traceback.print_exc())
        return None

multi_process_map_async(cmd_deal, tqdm(system_cmd_exec_arr))


