
**Description**


Every minute, the world loses an area of forest the size of 48 football fields. And deforestation in the Amazon Basin accounts for the largest share, contributing to reduced biodiversity, habitat loss, climate change, and other devastating effects. But better data about the location of deforestation and human encroachment on forests can help governments and local stakeholders respond more quickly and effectively.

Planet, designer and builder of the world’s largest constellation of Earth-imaging satellites, will soon be collecting daily imagery of the entire land surface of the earth at 3-5 meter resolution. While considerable research has been devoted to tracking changes in forests, it typically depends on coarse-resolution imagery from Landsat (30 meter pixels) or MODIS (250 meter pixels). This limits its effectiveness in areas where small-scale deforestation or forest degradation dominate.

Furthermore, these existing methods generally cannot differentiate between human causes of forest loss and natural causes. Higher resolution imagery has already been shown to be exceptionally good at this, but robust methods have not yet been developed for Planet imagery.

In this competition, Planet and its Brazilian partner SCCON are challenging Kagglers to label satellite image chips with atmospheric conditions and various classes of land cover/land use. Resulting algorithms will help the global community better understand where, how, and why deforestation happens all over the world - and ultimately how to respond.



**Approach**

- [x] Trained 10 models based on 10 fold cross validation method
- [x] Each of the models are of VGG19 architecture 
- [x] Started with the pretrained imageNet weights and fixed the 1st 10 layers so that they are not trained. Since we have less data don't want to 
   train the layers that learn generic features. The more the layers we train the greater is the chance of overfitting
- [x] Trained each model with varying learning rate
- [x] sklearn.metrics.fbeta_score is used to determine the threshold cutoff for each class 
- [x] If a class is voted by half of the models then that class is set.


*Kaggle link to the Competition*
https://www.kaggle.com/c/planet-understanding-the-amazon-from-space

*Kaggle link to the dataset*
https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data


*Kaggle Profile*
https://www.kaggle.com/santanuds


 
    


