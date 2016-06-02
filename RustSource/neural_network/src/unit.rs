use std::fmt::{self, Formatter, Display};

#[derive(Clone, Copy)]
pub struct Unit {
    // value computed in forward pass
    pub value: f32,
    // derivative of circuit output wrt this unit
    pub grad: f32,
}

impl Unit {
    pub fn new(v: f32, g: f32) -> Unit {
        Unit {
            value: v,
            grad: g,
        }
    }
}

impl Display for Unit {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(f, "Value: {}, Grad: {}", self.value, self.grad)
    }
}
