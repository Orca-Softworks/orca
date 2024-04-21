#[outputs] {
    let commanded_open = some_variable > some_const;
    // We dont want to continuously
    if (banked_output && !commanded_open) {
        out.set(False);
    } else {
        out.set(commanded_open);
    }
}

#[bank_controller] {
    // Every cycle, every time we ask this neuron, itll either change
    // its output name, or not, depending on the
    for valve in valves.iter() {
        // TODO: make sleep a network of its own, and only impl wait_until
        // which only accepts a true or false.
        sleep!(delay);

        out.set(valve.name);
    }
}

#[delayed] {
    // so what does this do? if we see the input boolean signal
    // fire, we then wait for the bank to allow us to output.
    if valve_input {
        wait_until!(bank_allow);
        out.set(valve_input);
    }
}