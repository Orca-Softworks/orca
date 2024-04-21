
class Input(Node):
    """_summary_

    Args:
        Node (_type_): _description_
    """

    def __init__(
        self,
        *args,
        # The type of the input. Can translate (sometimes) one type to
        # another.
        input_type,
        # The output we should listen to somewhere else in the graph.
        query=None,
        # If this input comes from an output somewhere later in the network.
        feedback=False,
        # If this input should resolve to multiple neurons.
        many=None,
        # The initial value, if this does not have a query
        initial_value=None,
        # If this value is really just a const.
        constant=False,
        # If we want to buffer values up to some count or duration.
        buffered=None,
        # We can average our value over some time period. Impl depends on
        # type.
        persistence=None,
        # we can auto generate an input that stores the latest write
        # time for us.
        save_latest_write_time=False,
        keeparound_duration="10_s",
        unit=None,
        track_disconnect=False,
        report_disconnect=False,
        big=False,
        **kwargs,
    ):
        Node.__init__(self, *args, **kwargs)

        # should be possible to come up with different translations schemes.
        self.input_type = input_type
        # If we should listen to some output.
        self.query = query
        # If this channel is fed back from a downstream calculation
        # into this one.
        self.feedback = feedback
        self.many = many
        self.initial_value = initial_value
        self.constant = constant
        self.buffered = buffered
        self.persistence = persistence
        self.save_latest_write_time = save_latest_write_time
        self.keeparound_duration = keeparound_duration
        self.unit = unit
        self.track_disconnect = track_disconnect
        self.report_disconnect = report_disconnect
        self.big = big

    def validate(self):
        super().validate()

        if self.query == None and self.initial_value == None:
            self.error("Cannot set query and initial value together.")

        if self.query != None and self.initial_value != None:
            self.error("Must set an initial value if there is not query.")

        # This input is going to have some set of resolved neurons based on its query.
        self._resolved_neurons = []

    def overview(self):
        return f"""
        {super().overview()}
        input_type: {self.input_type}
        query: {self.query}
        initial_value: {self.initial_value}
        """
