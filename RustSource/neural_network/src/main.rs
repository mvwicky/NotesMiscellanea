// http://karpathy.github.io/neuralnets/

extern crate rand;

mod unit;
mod gate;

use unit::Unit;
use gate::{AddGate, MultiplyGate, SigGate};

fn indent(size: usize) -> String {
    const INDENT: &'static str = "    ";
    (0..size)
        .map(|_| INDENT)
        .fold(String::with_capacity(size * INDENT.len()), |r, s| r + s)
}



struct Neuron {
    // f(a, b, c, x, y) = sig(ax+by+c)
    inp: (Unit, Unit, Unit, Unit, Unit),
    mulg: (MultiplyGate, MultiplyGate),
    addg: (AddGate, AddGate),
    sigg: SigGate,
    step_size: f32,
}

impl Neuron {
    fn new() -> Neuron {
        // a = 1, b = 2, c = -3, x = -1, y = 3
        Neuron {
            inp: (Unit::new(1.0, 0.0),
                  Unit::new(2.0, 0.0),
                  Unit::new(-3.0, 0.0),
                  Unit::new(-1.0, 0.0),
                  Unit::new(3.0, 0.0)),
            mulg: (MultiplyGate::new(), MultiplyGate::new()),
            addg: (AddGate::new(), AddGate::new()),
            sigg: SigGate::new(),
            step_size: 0.01,
        }
    }
    fn forward(&mut self) -> Unit {
        self.mulg.0.forward(self.inp.0, self.inp.3);
        self.mulg.1.forward(self.inp.1, self.inp.4);
        self.addg.0.forward(self.mulg.0.out, self.mulg.1.out);
        self.addg.1.forward(self.addg.0.out, self.inp.2);
        self.sigg.forward(self.addg.1.out)
    }
    fn backward(&mut self) {
        self.sigg.out.grad = 1.0;

        // sigg back
        let s = SigGate::sig(self.sigg.out.value);
        self.addg.1.out.grad += (s * (1.0 - s)) * self.sigg.out.grad;
        // addg1 back
        self.addg.0.out.grad += 1.0 * self.addg.1.out.grad;
        self.inp.2.grad += 1.0 * self.addg.1.out.grad;
        // addg0 back
        self.mulg.0.out.grad += 1.0 * self.addg.0.out.grad;
        self.mulg.1.out.grad += 1.0 * self.addg.0.out.grad;
        // mulg1 back
        self.inp.1.grad += self.inp.4.value * self.mulg.1.out.grad;
        self.inp.4.grad += self.inp.1.value * self.mulg.1.out.grad;
        // mulg0 back
        self.inp.0.grad += self.inp.3.value * self.mulg.0.out.grad;
        self.inp.3.grad += self.inp.0.value * self.mulg.0.out.grad;
        // adjust inputs
        self.inp.0.value += self.step_size * self.inp.0.grad;
        self.inp.1.value += self.step_size * self.inp.1.grad;
        self.inp.2.value += self.step_size * self.inp.2.grad;
        self.inp.3.value += self.step_size * self.inp.3.grad;
        self.inp.4.value += self.step_size * self.inp.4.grad;
    }
}


fn main() {
    let mut single = Neuron::new();
    single.forward();
    println!("{}", single.inp.0);
    println!("{}", single.inp.1);
    println!("{}", single.inp.2);
    println!("{}", single.inp.3);
    println!("{}", single.inp.4);
    println!(" ");
    println!("{}", single.mulg.0.out);
    println!("{}", single.mulg.1.out);
    println!("{}", single.addg.0.out);
    println!("{}", single.addg.1.out);
    println!("{}", single.sigg.out);
    single.backward();
    single.forward();
    println!(" ");
    println!("{}", single.mulg.0.out);
    println!("{}", single.mulg.1.out);
    println!("{}", single.addg.0.out);
    println!("{}", single.addg.1.out);
    println!("{}", single.sigg.out);
}
