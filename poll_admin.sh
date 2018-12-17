COMMAND=$1
QUEUE_SERVER=${2:-""}
OPAL_SERVER=${3:-"datashield_opal:8443"}
POLL_THREADS=${4:-""}

function getPollStatus() {

    if [ "" == "$(pgrep -f ds_poll.py)" ]; then 
        echo "Poll Stopped"
    else
        echo "Poll Running"
    fi
}

case "$COMMAND" in
            start )
            echo "Starting poll  with queue server: $QUEUE_SERVER, opal server: $OPAL_SERVER and number of poll threads: $POLL_THREADS"
            cd /root/ds_poll/ python3 ds_poll.py $QUEUE_SERVER $OPAL_SERVER -s -v $POLL_THREADS
            ;;
        
        stop )
            echo "Stopping poll ..."
            kill `pgrep -f ds_poll.py`
            ;;

        status )
            getPollStatus
            ;;
        
        * )
            echo $"Usage: $0 {start|stop|status|}"
            exit 1

esac
