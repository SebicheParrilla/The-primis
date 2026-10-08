# Photointerruptor


<div align= "center">
<img src="../../../hardware/photos/photointerruptor.jpg" width=250>
</div>

---

This is a T slot photointerruptor, in one side of the pilars making the slot, theres a infrared light emitter, and on the other side theres a phototransistor. When you interrupt the light from reaching the phototransistor the resulting electrical signal is sent to the LM393 comparator, which turns it into a clean digital HIGH/LOW signal, to be read by the microcontroller.

This component will be used as a RPM sensor, crutial to know the speed of our pneumtaic engine, to be later used when calculating gear ratios.