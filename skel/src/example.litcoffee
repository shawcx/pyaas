
    $(document).ready () ->
        console.log 'Ready'

Utility function to cancel an event

    window.cancelEvent ?= (event) ->
        event.preventDefault()
        event.stopPropagation()
        return false
