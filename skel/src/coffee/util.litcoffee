
Utility function to cancel an event

    window.cancelEvent ?= (event) ->
        event.preventDefault()
        event.stopPropagation()
        return false
