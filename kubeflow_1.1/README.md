# kubeflow-manifests

#### kfctl下载
    https://github.com/kubeflow/kfctl/releases/tag/v1.1.0

#### kustomize下载
    https://github.com/kubernetes-sigs/kustomize/releases/tag/kustomize%2Fv3.2.1

#### kfctl_istio_dex下载
    https://raw.githubusercontent.com/kubeflow/manifests/v1.1-branch/kfdef/kfctl_istio_dex.v1.1.0.yaml

#### kfctl_k8s_istio下载
    https://github.com/kubeflow/manifests/blob/master/kfdef/kfctl_k8s_istio.yaml
    
    
```

grep -o -h -R -E 'gcr.io/[a-zA-Z0-9/.@-]+:[a-zA-Z0-9.-]+' .cache | uniq |sort -u >> 'images_list'


```