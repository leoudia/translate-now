// https://adrianmejia.com/blog/2016/08/24/building-a-node-js-static-file-server-files-over-http-using-es6/

const http = require('http');
const url = require('url');
const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const port = process.argv[2] || 8080;

http.createServer(async function(req, res) {
  // console.log(`${req.method} ${req.url}`);

  // parse URL
  const parsedUrl = url.parse(req.url);
  // extract URL path
  let pathname = parsedUrl.pathname.replace("/widget/app", "");
  pathname = path.join(__dirname, 'app', pathname);

  // based on the URL path, extract the file extention. e.g. .js, .doc, ...
  const ext = path.parse(pathname).ext || '.html';
  // maps file extention to MIME typere
  const map = {
    '.ico': 'image/x-icon',
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.svg': 'image/svg+xml',
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
  };
  console.log(`Request for ${pathname} received.`);
  try {
    await fsp.access(pathname, fs.constants.F_OK);
    const stat = await fsp.stat(pathname);
    if (stat.isDirectory()) {
      pathname = path.join(pathname, '/index' + ext);
      await fsp.access(pathname, fs.constants.F_OK);
    }
    fs.readFile(pathname, function(err, data) {
      if (err) {
        res.statusCode = 500;
        res.end(`Error getting the file: ${err}.`);
      } else {
        // if the file is found, set Content-type and send data
        res.setHeader('Content-type', map[ext] || 'text/plain' );
        res.end(data);
      }
    });
  } catch (err) {
    res.statusCode = 404;
    console.error(err);
    res.end(`File ${pathname} not found!`);
  }
}).listen(parseInt(port));

// console.log(`Server listening on port ${port}`);
