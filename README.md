## Summary
- Traditional tracking models are vulnerable to occlusion, which causes identity switches when an object (person) is occluded by another object.
- This study uses two cameras to prevent identity switches for occluded objects.
- This study is conducted in an indoor space and involves two people.
- The idea is to enable tracking using two cameras without using a sophisticated object re-identification model such as deepsort.

## Limitation
- If an object is occluded and given a new ID, the issue is not resolved
- Therefore I'm going to use two cameras to address the case that the correct ID changes another ID beacuse of occlusion.

## References
- https://docs.ultralytics.com/modes/track/#available-trackers
- Enter the above website to Setting environment and Install requirements
