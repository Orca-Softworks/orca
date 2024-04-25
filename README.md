# Neuron

## Overview

Okay, Ive worked on this idea for not too long. But the sensations always been there that I dont like modern programming.

This project is just one of many steps Im taking on some path that might randomly end at some point when Im bored. But Ive been bugged for far too long
about the poor expressions we have in modern languages. I think generally structs and functions are good abstractions. But Im not sure Im a huge fan of them.
I also dont think functional programming, without a lot of extra layers is all that helpful. But I do like where it tries to get, with no side effects.
Some languages like Pkl have shown themselves to be closing in on how a language should feel.

Im gonna call what Im trying here network-oriented programming. We define neurons, with some set of inputs and a single output. We then define
networks, collections of neurons or other networks. The definition of the objects is separated from how we want to actually hook them into the
network. So when we declare an input to a neuron, it can be a query of multiple neurons from somewhere earlier in the network process chain. It
can also be some feedback from somewhere later in the process chain. But we dont need to have those neurons imported and used directly in the definition,
just query by name or by tag or some other element.

The reason a neuron is only one output is it helps us keep track of execution order/dependency within the network. It also helps enforce that
"single responsibility" rule people like. We can reason about this one thing. Networks are the part of the system that can have multiple inputs
and multiple outputs. You can then inside a network inside of a neuron to be used as part of its "implementation". Think of it as function nesting. You
are embedding an instance of the network inside the neuron.

You then pick a network to execute. If there are some missing initial_value's, the programm will ask you to supply values for them. Then
the network executes per how you defined it.

## Why

I truly think it sucks to work with computers. It doesnt feel right. Id much rather express how I want to solve a problem as some generic process
network, then "impl" it separate. What people dont realize about programming is that half of it is having a structure you can work off of reliably.
I think a language that helps with that could be impactful in a real way. You can also more easily visualize a program like this. It's natural
to look at a graph and see the directions of the arrows.

Generally, Im doing it just to prove to myself that theres an alternative to how we interact with computers today.

I really like async programming, but again a lack of structure for it can be really painful. Its also really painful to mix sync and async code.
I want this to be better handled in this language than in others.

Also, by starting with a neuron, I think its relatively fast to build a mental model of the shape of a network.

You can also build complicated structure out of the network itself. Each neuron can have a more primitive type. So instead of complicated
data structs, you build up network of inputs that represent an instance of a struct. Each neuron can still have some different type, but these
types can generally be as small as they need to be.

## Inspiration

My main inspiration is the brain. Most neurons are many input, single output. What if the brain chose that because it was the best way to manage
the complexity of the sorts of computations it is performing? And if its good enough for the brain, I think it's going to be good enough for us.

When you look at the brain, you see many structures that run in parallel with each other. This is especially prevalent in visual processing,
where you need to discretize the field of vision to extract information from it. But, and this is a suspicion, but we may see similar parallel processing
happening in predictive parts of the brain. Each one simulating a different outcome to a scenario. Whoever is closest gets the "prize", maybe some dopamine.

We are going to start building hardware for neural nets. If we dont want to just leave all the fun for the robots who program for us, I think we will
need a language we can adopt for expressing these neural nets ourselves.