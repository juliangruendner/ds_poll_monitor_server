COMMAND=$1
QUEUE_SERVER=${2:-""}
OPAL_SERVER=${3:-"-o datashield_opal:8443"}
POLL_THREADS=${4:-""}
CHECK_SERVER_CERT=${5:-""}

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
            cd /home/dspoll/ds_poll && python3 ds_poll.py $QUEUE_SERVER $OPAL_SERVER -s -v $POLL_THREADS $CHECK_SERVER_CERT
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
