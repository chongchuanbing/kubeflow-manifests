When profile-controller image updated, you can run below command to update it in manifest.

```
kustomize edit set image docker.io/chongchuanbing/kubeflow-images-public.profile-controller:vmaster-g34aa47c2:$NEW_TAG
```
