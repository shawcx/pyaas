
So the server has a ping -> pong, but it seemed easier for the clients to send
a ping instead of the server iterating over all the clients. The purpose is to
keep the connection alive in case some router timeouts the connection.

    class window.Socket
        constructor: (options) ->
            @options = $.extend
                timeout   : 0.9375
                maxtime   : 60
                path      : 'ws'
                ping      : false
                onmessage : () ->
                ontimeout : () ->
                    alert('Connection lost')
                    return
              ,
                options

            @timeout = @options.timeout

            @connect()
            return

        connect: () ->
            protocol = location.protocol.replace('http','ws')
            @ws = new WebSocket("#{protocol}//#{location.host}/#{@options.path}")

            @ws.onopen = (event) =>
                if @options.ping
                    @interval = setInterval () =>
                        @ws.send('ping')
                        return
                      ,
                        1000 * @options.ping
                return

On message from the server, dispatch it the event handler in Deploy. The
protocol is simply a JSON object of {action:'event', data:<arbirtary data>}.

            @ws.onmessage = (event) =>
                msg = JSON.parse(event.data)
                @options.onmessage(msg)
                return

            @ws.onerror = (event) =>
                clearInterval(@interval)
                @timeout = @timeout * 2
                return

            @ws.onclose = (event) =>
                clearInterval(@interval)

                if @timeout > @options.maxtime
                    console.warn('Unable to reconnect to server, giving up.')
                    @options.ontimeout()
                    return

                console.info('Connection closed, reconnecting in', Math.round(@timeout))

                setTimeout () =>
                    @connect()
                    return
                  ,
                    1000 * @timeout
                return

            return

Utility function to pass through to the underlying websocket

        send: () ->
            @ws.send.apply @ws, arguments
