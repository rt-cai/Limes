out="private"
mkdir $out
openssl genrsa -out $out/key.pem
openssl req -new -key $out/key.pem -out $out/csr.pem
openssl x509 -req -days 825 -in $out/csr.pem -signkey $out/key.pem -out $out/cert.pem
rm $out/csr.pem
