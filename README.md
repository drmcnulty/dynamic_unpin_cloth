# Dynamic Unpin Cloth
Addon for Blender that helps animators create unique effects combining Cloth Physics and Dynamic Paint.

What started as a tedious and manual physics/modifier stack setup evolved into a reusable addon for Blender-- my first! I wanted a way to destroy meshes without creating a separate set of meshes for the destruction event (e.g. cell fracture + rigid body), and without carefully re-applying Cloth + Vertex Weight Mix modifiers. In the cases of simple, far away, out of focus, or even for close up large-scale cloth destruction, Dynamically painting the destruction onto the object can save you time when exact control of the deformation is unnecessary.

Want to motivate me to make more code like this?

<a href="https://www.buymeacoffee.com/mcnulty" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>

https://user-images.githubusercontent.com/33881833/211217315-ffa9cdfb-8a16-4195-821b-2d3f05363d79.mp4

## Installation:
1. Download dynamic_unpin_cloth.py from the latest release : https://github.com/drmcnulty/dynamic_unpin_cloth/releases/download/DUC_1_0_0/dynamic_unpin_cloth.py
1. Open Blender Preferences (Edit > Preferences...) ![image](https://user-images.githubusercontent.com/33881833/211224843-d5b430ea-f382-4925-8bc5-d49a710d9b96.png)

1. Select the "Add-ons" section. ![image](https://user-images.githubusercontent.com/33881833/211224866-f857d650-aada-4269-ad16-b4d4be8448fb.png)

1. Click "Install..." ![image](https://user-images.githubusercontent.com/33881833/211224877-794aff1e-bcae-4383-9cac-352b15c80b53.png)

1. Browse to the file you downloaded and click on "Install Add-on"
1. Ensure that "Enabled Add-ons Only" is not checked, and that "Community" Add-ons are visible ![image](https://user-images.githubusercontent.com/33881833/211224899-420617ed-e0ec-4a0d-8472-a32772ad9448.png)
1. Search for "Dynamic Unpin Cloth" Check the box next to "Object: Dynamic Unpin Cloth" ![image](https://user-images.githubusercontent.com/33881833/211224952-17c86732-5ce1-4101-8a78-847a9682d2dd.png)
1. If you want Blender to keep this Add-on enabled next time you restart, click "Save Preferences" at the bottom.
![image](https://user-images.githubusercontent.com/33881833/211224759-dcf3b111-d494-4854-b11e-daa95aa4f342.png)

## Basic Usage:
There are 3 steps to adding Dynamic Unpin Cloth behaviour to a scene: 
1. Apply DUC to the affected object
1. make a second object into a brush
1. make the two objects interact.

### Apply Dynamic Unpin Cloth to a Mesh Object

Select the object(s) you want to turn into dynamically unpinnable cloth. In the Object menu, Click "Dynamic Unpin Cloth."
![image](https://user-images.githubusercontent.com/33881833/211606439-06fc5fcf-e668-4fc1-8a40-17e76275a07a.png)

### Create a Dynamic Paint Brush

Select a different object and add Physics->Dynamic Paint->Brush to it.
![image](https://user-images.githubusercontent.com/33881833/211607083-37158fcd-880a-4361-b45d-1e85a7568cf5.png)

### Animate

Animate the scene so that the Dynamic Paint Brush makes contact with the DUC object.
![duc_basic_usage](https://user-images.githubusercontent.com/33881833/211629394-9b53ade8-ba60-4145-bb3d-3903d8af95e1.gif)

## Tutorials:
### Particle System
### Animated Meshes
### Melting effect
### Shredding effect
### Tweaking the modifiers

## Demonstrations:

Applying Dynamic Unpin Cloth to a Mesh object with default cloth behaviour:

https://user-images.githubusercontent.com/33881833/211219541-5bd37e79-7720-4c78-8f0e-7ace2d88f29a.mp4




Applying Dynamic Unpin Cloth to a Mesh object that has pre-made edge-split knife-cuts across its topology:

https://user-images.githubusercontent.com/33881833/211219560-3bab8d36-1e4d-4718-b9e1-4f71435d4e3f.mp4



Effect realized by checking the "Shatter" option in the Dynamic Unpin Cloth operation menu.

https://user-images.githubusercontent.com/33881833/211219591-1ed974c5-c0f3-490d-a358-6ef29a389738.mp4

