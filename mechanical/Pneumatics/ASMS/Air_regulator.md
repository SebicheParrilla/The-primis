# Air regulator 

The Pneumatic engine that powers our robot needs a reliable and constant supply of air pressure, the regulator is escencial for this.

<div align= "center">
<img src="../../../../hardware/photos/regulator.png" width=330>

</div>

---

For the pneumatic engine needs **20-25PSI** of pressure to operate, but thanks to [this test](../../../../logs/tests/air_supply_duration_calculations.md), we knew that we needed to store up to **100PSI** worth of air in the tanks. But we can't just supply **100PSI** to the engine, it'll start to spin fast and even burst some silicone hoses, we need something to control the pressure being supplied to the pneumatic engine, and that's where the regulator comes in.

The regulator allows you to control the maximum pressure that is going to come out of the outlet, this lets us have a high pressure side and a adjustable low pressure side.