# kubeflow-manifests

#### kfctl下载
    https://github.com/kubeflow/kfctl/releases/tag/v1.1.0

#### kustomize下载
    https://github.com/kubernetes-sigs/kustomize/releases/tag/kustomize%2Fv3.2.1

#### kfctl_istio_dex下载
    https://raw.githubusercontent.com/kubeflow/manifests/v1.1-branch/kfdef/kfctl_istio_dex.v1.1.0.yaml

#### kfctl_k8s_istio下载
    https://github.com/kubeflow/manifests/blob/master/kfdef/kfctl_k8s_istio.yaml
    
#### 找出镜像列表    
```
grep -o -h -R -E 'gcr.io/[a-zA-Z0-9/.@-]+:[a-zA-Z0-9.-]+' .cache | uniq |sort -u >> 'images_list'
```

#### 镜像处理
    python image_deal.py
    

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