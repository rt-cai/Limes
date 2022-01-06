ca_name="CA"

mkdir certFiles
cd certFiles
openssl genrsa -out $ca_name.key -des3 4096
openssl req -x509 -sha256 -new -nodes -days 3650 -key $ca_name.key -out $ca_name.pem \
    -subj "/C=CA/ST=BC/L=Vancouver/O=Hallam Lab/OU=Limes/CN="