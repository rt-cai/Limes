ca_name="CA"
# domain="computeCanada"
domain="localhost"
pair_name="for_server"

dir=certFiles/$domain
mkdir $dir
cd $dir

openssl genrsa -out $domain.key 4096
openssl req -new -key $domain.key -out $domain.csr \
    -subj "/C=CA/ST=BC/L=Vancouver/O=Hallam Lab/OU=Limes/CN=limes-portal"

openssl x509 -req -in $domain.csr -CA ../$ca_name.pem -CAkey ../$ca_name.key -CAcreateserial -days 3650 -sha256 \
    -extfile ../../info/$domain.ext \
    -out $pair_name.crt
openssl rsa -in $domain.key -out $pair_name.key