const fs = require("fs");
const jwt = require("jsonwebtoken");

const privateKey = fs.readFileSync("AuthKey_NXHCF4VY9Z.p8").toString();
const teamId = "48N7BQ4S2H";
const keyId = "NXHCF4VY9Z";

const jwtToken = jwt.sign({}, privateKey, {
  algorithm: "ES256",
  expiresIn: "180d",
  issuer: teamId,
  header: {
    alg: "ES256",
    kid: keyId,
  },
});

console.log(jwtToken);
