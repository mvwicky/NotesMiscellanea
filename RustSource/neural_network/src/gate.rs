
use unit::Unit;

pub struct MultiplyGate {
    pub inp: (Unit, Unit),
    pub out: Unit,
}

pub struct AddGate {
    pub inp: (Unit, Unit),
    pub out: Unit,
}

pub struct SigGate {
    pub inp: Unit,
    pub out: Unit,
}

impl MultiplyGate {
    pub fn new() -> MultiplyGate {
        MultiplyGate {
            inp: (Unit::new(0.0, 0.0), Unit::new(0.0, 0.0)),
            out: Unit::new(0.0, 0.0),
        }
    }
    pub fn forward(&mut self, u0: Unit, u1: Unit) -> Unit {
        self.inp.0 = u0;
        self.inp.1 = u1;
        self.out = Unit::new((self.inp.0.value * self.inp.1.value), 0.0);
        self.out
    }
}

impl AddGate {
    pub fn new() -> AddGate {
        AddGate {
            inp: (Unit::new(0.0, 0.0), Unit::new(0.0, 0.0)),
            out: Unit::new(0.0, 0.0),
        }
    }
    pub fn forward(&mut self, u0: Unit, u1: Unit) -> Unit {
        self.inp.0 = u0;
        self.inp.1 = u1;
        self.out = Unit::new((self.inp.0.value + self.inp.1.value), 0.0);
        self.out
    }
}

impl SigGate {
    pub fn new() -> SigGate {
        SigGate {
            inp: Unit::new(0.0, 0.0),
            out: Unit::new(0.0, 0.0),
        }
    }
    pub fn sig(x: f32) -> f32 {
        1.0 / (1.0 + (-x).exp())
    }
    pub fn forward(&mut self, u0: Unit) -> Unit {
        self.inp = u0;
        self.out = Unit::new(SigGate::sig(self.inp.value), 0.0);
        self.out
    }
}
