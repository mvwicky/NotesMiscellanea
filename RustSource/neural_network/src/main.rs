// http://karpathy.github.io/neuralnets/

extern crate rand;

use std::f32;
// use rand::Rng;
// use std::collections::HashMap;
use std::fmt::{self, Formatter, Display};

fn indent(size: usize) -> String {
    const INDENT: &'static str = "    ";
    (0..size)
        .map(|_| INDENT)
        .fold(String::with_capacity(size * INDENT.len()), |r, s| r + s)
}

/*fn forward_multiply_gate(_x: f32, _y: f32) -> f32 {
    _x * _y
}

fn forward_add_gate(_x: f32, _y: f32) -> f32 {
    _x + _y
}

fn random_local_search(x: f32, y: f32) {
    println!("Random Local Search");
    let mut rng = rand::thread_rng();
    let tweak_amount = 0.01;
    let mut best_out = f32::NEG_INFINITY;
    let mut best_x = x;
    let mut best_y = y;
    for _ in 0..10 {
        let x_try = x + tweak_amount * (rng.gen::<f32>() * 2.0 - 1.0);
        let y_try = y + tweak_amount * (rng.gen::<f32>() * 2.0 - 1.0);
        let out = forward_multiply_gate(x_try, y_try);
        if out > best_out {
            best_out = out;
            best_x = x_try;
            best_y = y_try;
        }
    }
    println!("Best Output: {}", best_out);
    println!("Best (x , y) = ({} , {})", best_x, best_y);
    println!(" ");
}

fn numerical_gradient(x: f32, y: f32) {
    println!("Numerical Gradient");
    let out = forward_multiply_gate(x, y);
    println!("Original Output: {}", out);
    let h = 0.0001;
    let step_size = 0.01;

    let xph = x + h;
    let out_x = forward_multiply_gate(xph, y);
    let x_derivative = (out_x - out) / h;

    let yph = y + h;
    let out_y = forward_multiply_gate(x, yph);
    let y_derivative = (out_y - out) / h;

    let new_x = x + step_size * x_derivative;
    let new_y = y + step_size * y_derivative;

    let out_new = forward_multiply_gate(new_x, new_y);
    println!("New Output: {}", out_new);
    println!(" ");
}

fn analytic_gradient(x: f32, y: f32) {
    println!("Analytic Gradient");
    println!("Original Output: {}", forward_multiply_gate(x, y));
    let step_size = 0.01;
    let x_gradient = y;
    let y_gradient = x;

    let new_x = x + step_size * x_gradient;
    let new_y = y + step_size * y_gradient;
    let out_new = forward_multiply_gate(new_x, new_y);
    println!("New Output: {}", out_new);
    println!(" ");
}

fn recursive_case(x: f32, y: f32, z: f32) {
    println!("Recursive Case");
    let q = forward_add_gate(x, y);
    let f = forward_multiply_gate(q, z);

    println!("Original Output: {}", f);

    // gradient of multiply gate wrt. inputs
    let deriv_f_wrt_z = q;
    let deriv_f_wrt_q = z;

    // gradient of add gate wrt. inputs
    let deriv_q_wrt_x = 1.0;
    let deriv_q_wrt_y = 1.0;

    // chain rule
    let deriv_f_wrt_x = deriv_q_wrt_x * deriv_f_wrt_q;
    let deriv_f_wrt_y = deriv_q_wrt_y * deriv_f_wrt_q;

    let grad = [deriv_f_wrt_x, deriv_f_wrt_y, deriv_f_wrt_z];

    println!("Gradient: ({}, {}, {})", grad[0], grad[1], grad[2]);

    let step_size = 0.01;
    let new_x = x + step_size * deriv_f_wrt_x;
    let new_y = y + step_size * deriv_f_wrt_y;
    let new_z = z + step_size * deriv_f_wrt_z;

    let q = forward_add_gate(new_x, new_y);
    let f = forward_multiply_gate(q, new_z);
    println!("New Output: {}", f);
    println!(" ");
}*/

#[derive(Clone, Copy)]
struct Unit {
    // value computed in forward pass
    value: f32,
    // derivative of circuit output wrt this unit
    grad: f32,
}

impl Unit {
	fn new(v: f32, g: f32) -> Unit {
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

struct MultiplyGate {
    u0: Unit,
    u1: Unit,
    utop: Unit,
}

impl MultiplyGate {
    fn new() -> MultiplyGate {
        MultiplyGate {
        	u0: Unit::new(0.0, 0.0),
        	u1: Unit::new(0.0, 0.0),
        	utop: Unit::new(0.0, 0.0),
        }
    }
    fn forward(&mut self, u0: Unit, u1: Unit) -> Unit {
        self.u0 = u0;
        self.u1 = u1;
        self.utop = Unit::new((self.u0.value * self.u1.value), 0.0);
        self.utop
    }
    fn backward(&mut self) {
        self.u0.grad += self.u1.value * self.utop.grad;
        self.u1.grad += self.u0.value * self.utop.grad;
    }
}

struct AddGate {
    u0: Unit,
    u1: Unit,
    utop: Unit,
}

impl AddGate {
    fn new() -> AddGate {
        AddGate {
        	u0: Unit::new(0.0, 0.0),
        	u1: Unit::new(0.0, 0.0),
        	utop: Unit::new(0.0, 0.0),
        }
    }
    fn forward(&mut self, u0: Unit, u1: Unit) -> Unit {
        self.u0 = u0;
        self.u1 = u1;
        self.utop = Unit::new((self.u0.value + self.u1.value), 0.0);
        self.utop
    }
    fn backward(&mut self) {
        self.u0.grad += 1.0 * self.utop.grad;
        self.u1.grad += 1.0 * self.utop.grad;
    }
}

struct SigmoidGate {
    u0: Unit,
    utop: Unit,
}

impl SigmoidGate {
    fn sig(x: f32) -> f32 {
        1.0 / (1.0 + (-x).exp())
    }
    fn new() -> SigmoidGate {
        SigmoidGate {
        	u0: Unit::new(0.0, 0.0),
        	utop: Unit::new(0.0, 0.0),
        }
    }
    fn forward(&mut self, u0: Unit) -> Unit {
        self.u0 = u0;
        self.utop = Unit::new(SigmoidGate::sig(self.u0.value), 0.0);
        self.utop
    }
    fn backward(&mut self) {
        let s = SigmoidGate::sig(self.u0.value);
        self.u0.grad += (s * (1.0 - s)) * self.utop.grad;
    }
}

struct SingleNeuron {
	inputs: Vec<Unit>,
	mulg: Vec<MultiplyGate>,
	addg: Vec<AddGate>,
	sg: SigmoidGate,
	step_size: f32,
}

impl SingleNeuron {
	fn new() -> SingleNeuron {
		SingleNeuron{
			inputs: vec![],
			mulg: vec![],
			addg: vec![],
			sg: SigmoidGate::new(),
			step_size: 0.01,
		}
	}
	fn forward(&mut self) -> Unit {
		self.mulg[0].forward(self.inputs[0], self.inputs[3]); // ax
		self.mulg[1].forward(self.inputs[1], self.inputs[4]); // by
		let axpby = self.addg[0].forward(self.mulg[0].utop, self.mulg[1].utop);
		self.addg[1].forward(axpby, self.inputs[2]); // axpbypc
		self.sg.forward(self.addg[1].utop)
	}
	// mulg0.u0 = a           mulg0.u1 = x           mulg0.utop = ax
	// mulg1.u0 = b           mulg1.u1 = y           mulg1.utop = by
	// addg0.u0 = mulg0.utop  addg0.u1 = mulg1.utop  addg0.utop = ax+by 
	// addg1.u0 = addg0.utop  addg1.u1 = c           addg1.utop = ax+by+c
	// sg.u0    = addg1.utop  sg.utop  = sig(ax+by+c)     
	fn backward(&mut self, new_grad: f32) {
		self.sg.utop.grad = new_grad;
		// sg.backward
		let s = SigmoidGate::sig(self.sg.utop.value);
		self.addg[1].utop.grad += (s * (1.0 - s)) * self.sg.utop.grad;
		// addg1.backward
		self.addg[0].utop.grad += 1.0 * self.addg[1].utop.grad;
		self.inputs[2].grad += 1.0 * self.addg[1].utop.grad;
		// addg0.backward
		self.mulg[0].utop.grad += 1.0 * self.addg[0].utop.grad;
		self.mulg[1].utop.grad += 1.0 * self.addg[0].utop.grad;
		// mulg1.backward
		self.inputs[1].grad += self.inputs[4].value * self.mulg[1].utop.grad;  
		self.inputs[4].grad += self.inputs[1].value * self.mulg[1].utop.grad;
		// mulg0.backward
		self.inputs[0].grad += self.inputs[3].value * self.mulg[0].utop.grad;
		self.inputs[3].grad += self.inputs[0].value * self.mulg[0].utop.grad;

		self.inputs[0].value += self.step_size * self.inputs[0].grad;
		self.inputs[1].value += self.step_size * self.inputs[1].grad;
		self.inputs[2].value += self.step_size * self.inputs[2].grad;
		self.inputs[3].value += self.step_size * self.inputs[3].grad;
		self.inputs[4].value += self.step_size * self.inputs[4].grad;

	}
	fn print_input_state(&self) {
		println!("Input State");
		println!("a: {}", self.inputs[0]);
		println!("b: {}", self.inputs[1]);
		println!("c: {}", self.inputs[2]);
		println!("x: {}", self.inputs[3]);
		println!("y: {}", self.inputs[4]);
	}
	fn print_gate_state(&self) {
		println!("Gate State");
		println!("mulg0:");
		println!("{}u0:   {}", indent(1), self.mulg[0].u0);
		println!("{}u1:   {}", indent(1), self.mulg[0].u1);
		println!("{}utop: {}", indent(1), self.mulg[0].utop);
		println!("mulg1:");
		println!("{}u0:   {}", indent(1), self.mulg[1].u0);
		println!("{}u1:   {}", indent(1), self.mulg[1].u1);
		println!("{}utop: {}", indent(1), self.mulg[1].utop);
		println!("addg0:");
		println!("{}u0:   {}", indent(1), self.addg[0].u0);
		println!("{}u1:   {}", indent(1), self.addg[0].u1);
		println!("{}utop: {}", indent(1), self.addg[0].utop);
		println!("addg1:");
		println!("{}u0:   {}", indent(1), self.addg[1].u0);
		println!("{}u1:   {}", indent(1), self.addg[1].u1);
		println!("{}utop: {}", indent(1), self.addg[1].utop);
		println!("sg:");
		println!("{}u0:   {}", indent(1), self.sg.u0);
		println!("{}utop: {}", indent(1), self.sg.utop);
	}
}

fn single_neuron() {
    println!("Single Neuron");
    let mut neuron = SingleNeuron::new();
    neuron.inputs.push(Unit::new(1.0, 0.0));   // a
    neuron.inputs.push(Unit::new(2.0, 0.0));   // b
    neuron.inputs.push(Unit::new(-3.0, 0.0));  // c
    neuron.inputs.push(Unit::new(-1.0, 0.0));  // x
    neuron.inputs.push(Unit::new(3.0, 0.0));   // y
    
    neuron.mulg.push(MultiplyGate::new()); // mulg0
    neuron.mulg.push(MultiplyGate::new()); // mulg1

    neuron.addg.push(AddGate::new()); // addg0
    neuron.addg.push(AddGate::new()); // addg1

	neuron.forward();
    println!("After First Forward");
   	neuron.print_gate_state();

   	neuron.backward(0.01);
   	println!("After backprop");
   	neuron.print_input_state();

    neuron.forward();
    println!("After 2nd Forward");
    neuron.print_gate_state();

    println!(" ");
}


fn main() {
    /*random_local_search(-2.0, 3.0);
    numerical_gradient(-2.0, 3.0);
    analytic_gradient(-2.0, 3.0);
    recursive_case(-2.0, 5.0, -4.0);*/
    single_neuron();
}
