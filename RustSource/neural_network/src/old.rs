use rand::Rng;
use std::collections::HashMap;

fn forward_multiply_gate(_x: f32, _y: f32) -> f32 {
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
}