function Bird() {
  this.y = 300;
  this.x = 64;

  this.gravity = 0.7;
  this.lift = -12;
  this.velocity = -12;

  this.show = function() {
    fill(255);
    image(birdImg, this.x, this.y, 56, 48);
  };

  this.up = function() {
    this.velocity += this.lift;
    flapSound.play()
  };

  this.update = function() {
    this.velocity += this.gravity;
    // this.velocity *= 0.9;
    this.y += this.velocity;

    if (this.y > 721) {
      this.y = 721;
      this.velocity = 0;
    }

    if (this.y < 0) {
      this.y = 0;
      this.velocity = 0;
    }
  };
}
            