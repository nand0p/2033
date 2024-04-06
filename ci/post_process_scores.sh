#/bin/bash -ex


HTML=1
DOWNLOAD=0
UPLOAD=0
DEBUG=0


SOURCE_BUCKET=2030.hex7.com
DEST_BUCKET=2033.hex7.com
S3_PREFIX="scores"
TMP_DIR="./tmp"
mkdir -pv ${TMP_DIR}


SCORES_LIST=$(aws s3 ls s3://${DEST_BUCKET}/${S3_PREFIX}/ | cut -d' ' -f9)
#SCORES_LIST=$(aws s3 ls s3://${SOURCE_BUCKET}/${S3_PREFIX}/ | cut -d' ' -f9)


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
  echo "<h1>SCORES DATA</h1><p><br><p>" | tee ${TMP_DIR}/index.html >/dev/null
fi


for SCORES_FILE in ${SCORES_LIST}; do
  echo "====> SCORES_FILE: ${SCORES_FILE}"

  if [[ "${DOWNLOAD}" == "1" ]]; then
    aws s3 cp s3://${SOURCE_BUCKET}/${S3_PREFIX}/${SCORES_FILE} ${TMP_DIR}/${SCORES_FILE}
    echo "======> copy from source success"
  fi

  if [[ "${UPLOAD}" == "1" ]]; then
    aws s3 cp --acl public-read ${TMP_DIR}/${SCORES_FILE} s3://${DEST_BUCKET}/${S3_PREFIX}/${SCORES_FILE}
    echo "======> copy to dest success"
  fi

  if [[ "${HTML}" == "1" ]]; then
    echo "<a href=http://${DEST_BUCKET}/${S3_PREFIX}/${SCORES_FILE}>${SCORES_FILE}</a><br>" |tee -a ${TMP_DIR}/index.html >/dev/null
    echo "======> generate html success"
  fi

done


if [[ "${HTML}" == "1" ]]; then
  echo "</body></html>" | tee -a ${TMP_DIR}/index.html >/dev/null
  aws s3 cp --acl public-read ${TMP_DIR}/index.html s3://${DEST_BUCKET}/${S3_PREFIX}/index.html
fi


echo
echo scores transfer success
echo
