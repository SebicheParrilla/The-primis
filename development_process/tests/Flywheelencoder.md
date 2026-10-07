# Flywheel RPM sensor code testing

We need a reliable way to know the pneumatic engine's speed, we are using the [photointerruptor](../../../hardware/electrical/Cytron_Motion_2350_Pro/Photointerruptor.md) to count the gaps on our flywheel.

- We started the code by making a counter go up by every time the sensor goes from HIGH to LOW.   
[see here](../../../code/srs/flywheelencodercounter.py)

- Then we added a timer to print the time interval between every pulse.             
[see here](../../../code/srs/Flywheelencodertimer.py)

- Now we keep the timeintervals and store them in a sample queue, this basically stores 7 samples and every time theres a new one it deletes the oldest one, by doing the average between the 7 we can have a average reading of time intervals.                           
[see here](../../../code/srs/Flywheelencoder7sample.py)

- Here we simply added a timeout, that changed samples to 0 when a time interval max is reached, this allows the average  reading go to 0 whenthe engine is stopped.    
[see here](../../../code/srs/Flywheelencoder0timeout.py)

- And finally, calculate the RPM with the calculated average time interval with this formula:



    $$
    RPM = \frac{60,000,000}{t}
    $$

    Where:

    - $t$ = time interval between pulses in microseconds ($\mu s$)
    - $RPM$ = revolutions per minute

    [see here](../../../code/srs/FlywheelencoderRPM.py)