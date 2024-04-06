#/bin/bash -ex

DEBUG=0
DOWNLOAD=0
UPLOAD=0
HTML=0
SOURCE_BUCKET=2030.hex7.com
DEST_BUCKET=2033.hex7.com
SCORES_LIST=$(aws s3 ls s3://${SOURCE_BUCKET}/scores/ | cut -d' ' -f9)
TMP_DIR="./tmp"
mkdir -pv ${TMP_DIR}

echo
echo "scores transfer init"
echo

if [[ "${DEBUG}" == "1" ]]; then
  echo "==> DEBUG ${DEBUG}"
  echo "==> SCORES_LIST ${SCORES_LIST}"
  echo
fi

echo
echo "==> SOURCE_BUCKET ${SOURCE_BUCKET}"
echo "==> DEST_BUCKET ${DEST_BUCKET}"
echo

if [[ "${HTML}" == "1" ]]; then
  echo "<html><head><title>scores</title><body>" | tee ${TMP_DIR}/index.html >/dev/null
fi

for SCORES_FILE in ${SCORES_LIST}; do
  echo "====> SCORES_FILE: ${SCORES_FILE}"

  if [[ "${DOWNLOAD}" == "1" ]]; then
    aws s3 cp s3://${SOURCE_BUCKET}/scores/${SCORES_FILE} ${TMP_DIR}/${SCORES_FILE}
    echo "======> copy from source success"
  fi

  if [[ "${UPLOAD}" == "1" ]]; then
    aws s3 cp --acl public-read ${TMP_DIR}/${SCORES_FILE} s3://${DEST_BUCKET}/scores/${SCORES_FILE}
    echo "======> copy to dest success"
  fi

  if [[ "${HTML}" == "1" ]]; then
    echo "<a href=/scores/${SCORES_FILE}>${SCORES_FILE}</a>" |tee -a ${TMP_DIR}/index.html >/dev/null
    echo "======> generate html success"
  fi

done

if [[ "${HTML}" == "1" ]]; then
  echo "</body></html>" | tee -a ${TMP_DIR}/index.html >/dev/null
fi

echo
echo scores transfer success
echo
