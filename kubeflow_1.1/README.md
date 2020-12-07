# kubeflow-manifests

###目录介绍
```
 -- kubeflow_1.1
 ---- .cache                    kfctl build后下载解压的kubeflow manifests
 ---- kustomize                 kustomize build后生成的
 ---- kustomize_v3_support      kustomize v3兼容性修改的
 ---- yaml                      最后生成的kubeflow部署的yaml
 ---- image_deal.py             
 ---- image_list
 ---- 
```

### 工具下载

- kfctl下载
https://github.com/kubeflow/kfctl/releases/tag/v1.1.0

- kustomize下载
https://github.com/kubernetes-sigs/kustomize/releases/tag/kustomize%2Fv3.2.1

- kfctl_istio_dex下载
https://raw.githubusercontent.com/kubeflow/manifests/v1.1-branch/kfdef/kfctl_istio_dex.v1.1.0.yaml

- kfctl_k8s_istio下载
https://github.com/kubeflow/manifests/blob/master/kfdef/kfctl_k8s_istio.yaml

- kubeflow manifests
https://github.com/kubeflow/manifests/archive/v1.1.0.tar.gz
    
#### 版本介绍
| 版本 | 说明 |
| --- | --- |
| kfctl_istio_dex.v1.1.0.yaml | 多租户授权版 |
| kfctl_k8s_istio.v1.1.0.yaml | 单用户版 |
    
#### build
> * 会先下载 yaml中配置的kubeflow manifests压缩包
> * 解压到当前目录下 .cache 目录下

> * 如果自行下载压缩包，请修改 kfctl_istio_dex.v1.1.0.yaml 中的manifests url为 file:///{your path}/v1.0.2.tar.gz
> * 如果自行下载并解压了，请修改 kfctl_istio_dex.v1.1.0.yaml,在最后添加
    
    ```
    status:
      reposCache:
      - localPath: '"{你的解压路径}"'
        name: manifests
    ```

```
./kfctl_mac build -V -f kfctl_istio_dex.v1.1.0.yaml
```
    
#### 找出镜像列表    
```
grep -o -h -R -E 'gcr.io/[a-zA-Z0-9./_@-]+:[a-zA-Z0-9./_-]+' .cache | uniq |sort -u > 'images_list'
```

#### kustomize3 兼容性问题
```
cp -r -f ./kustomize_v3_support/ .cache/
```

#### 镜像处理
    python image_deal.py
    
#### 手动替换某些配置    
```
grep -rl "gcr.io/kfserving/sklearnserver" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?gcr.io/kfserving/sklearnserver?docker.io/chongchuanbing/ai/kfserving.sklearnserver?"
grep -rl "gcr.io/kfserving/xgbserver" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?gcr.io/kfserving/xgbserver?docker.io/chongchuanbing/ai/kfserving.xgbserver?"
grep -rl "gcr.io/kfserving/pytorchserver" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?gcr.io/kfserving/pytorchserver?docker.io/chongchuanbing/ai/kfserving.pytorchserver?"
grep -rl "gcr.io/kfserving/tensorrtserver" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?gcr.io/kfserving/tensorrtserver?docker.io/chongchuanbing/ai/kfserving.tensorrtserver?"
```

#### 在kustomize/knative/kustomize.yaml 中添加
```
images:
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.activator
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.activator
  newTag: lastest
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.autoscaler-hpa
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.autoscaler-hpa
  newTag: lastest
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.autoscaler
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.autoscaler
  newTag: lastest
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.networking.istio
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.networking.istio
  newTag: lastest
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.webhook
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.webhook
  newTag: lastest
- name: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.controller
  newName: docker.io/chongchuanbing/ai/knative-releases.knative.dev.serving.cmd.controller
  newTag: lastest
```

#### 镜像拉取策略修改
```
grep -rl "imagePullPolicy: Always" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?imagePullPolicy: Always?imagePullPolicy: IfNotPresent?"
```

#### 部分镜像手动修改
```
部分镜像上传到docker.io后，使用的 '.' 进行分隔，所以将 '/' 替换一下
grep -rl ".hub }}/{{ .Values." .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?.hub }}/{{ .Values.?.hub }}.{{ .Values.?"
grep -rl "gcr.io/istio-release" .cache/manifests/manifests-1.1-branch | xargs sed -i "" "s?gcr.io/istio-release?docker.io/chongchuanbing/ai/istio-release?"
```

#### 修改以下文件，添加workgroup的默认ServiceAccount的创建，没有该SA，登陆时创建租户有问题
    kubeflow_1.1/.cache/manifests/manifests-1.1-branch/pipeline/installs/multi-user/pipelines-profile-controller/sync.py
    
```
{
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "name": "default-editor",
        "namespace": namespace
    },
    "secrets": {
        "name": "default-token-kqvkn"
    }
},
```

#### yaml build 
```
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/application | tee yaml/application.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/bootstrap | tee yaml/bootstrap.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/cert-manager| tee yaml/cert-manager.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/cert-manager-crds| tee yaml/cert-manager-crds.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/cert-manager-kube-system-resources | tee yaml/cert-manager-kube-system-resources.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/cluster-local-gateway | tee yaml/cluster-local-gateway.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/dex | tee yaml/dex.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/istio | tee yaml/istio.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/istio-stack | tee yaml/istio-stack.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/kfserving| tee yaml/kfserving.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/knative | tee yaml/knative.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/kubeflow-apps | tee yaml/kubeflow-apps.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/metacontroller | tee yaml/metacontroller.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/namespaces | tee yaml/namespaces.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/oidc-authservice | tee yaml/oidc-authservice.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize/spark-operator | tee yaml/spark-operator.yaml
```

```
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/profiles | tee yaml_split/profiles.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/admission-webhook | tee yaml_split/admission-webhook.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/centraldashboard | tee yaml_split/centraldashboard.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/jupyter-web-app | tee yaml_split/jupyter-web-app.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/notebook-controller | tee yaml_split/notebook-controller.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/katib-crds | tee yaml_split/katib-crds.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/katib-controller | tee yaml_split/katib-controller.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/katib-db-manager | tee yaml_split/katib-db-manager.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/katib-db-mysql | tee yaml_split/katib-db-mysql.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/argo | tee yaml_split/argo.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/pipeline-minio | tee yaml_split/pipeline-minio.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/pipeline-multi-user | tee yaml_split/pipeline-multi-user.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/pipeline-mysql | tee yaml_split/pipeline-mysql.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/metadata | tee yaml_split/metadata.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/mpi-operator | tee yaml_split/mpi-operator.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/mxnet-operator | tee yaml_split/mxnet-operator.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/pytorch-operator | tee yaml_split/pytorch-operator.yaml
./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/tf-operator | tee yaml_split/tf-operator.yaml

./kustomize_kustomize.v3.2.1_darwin_amd64 build kustomize_split/selon-core-operator | tee yaml_split/selon-core-operator.yaml

```

#### deploy

```
kubectl apply -f .
```

```
kubectl apply -f namespaces.yaml
kubectl apply -f istio-stack.yaml
kubectl apply -f istio.yaml
kubectl apply -f cert-manager-crds.yaml
kubectl apply -f cert-manager-kube-system-resources.yaml
kubectl apply -f cert-manager-crds.yaml
kubectl apply -f application.yaml
kubectl apply -f cert-manager.yaml
kubectl apply -f dex.yaml
kubectl apply -f cluster-local-gateway.yaml
kubectl apply -f oidc-authservice.yaml
kubectl apply -f metacontroller.yaml
kubectl apply -f bootstrap.yaml
kubectl apply -f knative.yaml
kubectl apply -f kfserving.yaml
kubectl apply -f kubeflow-apps.yaml
kubectl apply -f spark-operator.yaml
```

```
kubectl apply -f namespaces.yaml
kubectl apply -f pv.yaml
kubectl apply -f istio-stack.yaml
kubectl apply -f istio.yaml
kubectl apply -f pvc.yaml
kubectl apply -f metacontroller.yaml
kubectl apply -f application.yaml
kubectl apply -f oidc-authservice.yaml
kubectl apply -f dex.yaml
kubectl apply -f cert-manager-crds.yaml
kubectl apply -f cert-manager-kube-system-resources.yaml
kubectl apply -f cert-manager-crds.yaml
kubectl apply -f cert-manager.yaml
kubectl apply -f cluster-local-gateway.yaml
kubectl apply -f bootstrap.yaml
kubectl apply -f knative.yaml
kubectl apply -f kfserving.yaml
kubectl apply -f profiles.yaml
kubectl apply -f admission-webhook.yaml
kubectl apply -f centraldashboard.yaml
kubectl apply -f jupyter-web-app.yaml
kubectl apply -f notebook-controller.yaml
kubectl apply -f pytorch-operator.yaml
kubectl apply -f tf-operator.yaml
kubectl apply -f mxnet-operator.yaml
kubectl apply -f mpi-operator.yaml
kubectl apply -f katib-crds.yaml
kubectl apply -f katib-db-mysql.yaml
kubectl apply -f katib-db-manager.yaml
kubectl apply -f katib-controller.yaml
kubectl apply -f pipeline-mysql.yaml
kubectl apply -f pipeline-minio.yaml
kubectl apply -f pipeline-multi-user.yaml
kubectl apply -f argo.yaml
kubectl apply -f selon-core-operator.yaml
kubectl apply -f metadata.yaml
kubectl apply -f spark-operator.yaml
```