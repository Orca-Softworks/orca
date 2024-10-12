#[delayed_output] {
    // so what does this do? if we see the input boolean signal
    // fire, we then wait for the bank to allow us to output.
    sleep!(delay);

    return output_to_delay;
}