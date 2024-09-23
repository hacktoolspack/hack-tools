// Stratified JS Standalone Library
// Version 0.3
// See http://www.croczilla.com/stratified for more info.
// (c) 2009 Alexander Fritze <alex@croczilla.com>
//
// This file is licensed under the terms of the GNU GPL version 2.
//
// Contains a JavaScript parser based on the Narcissus JS engine code,
// written by Brendan Eich with several modifications made by Neil Mix
// as part of Narrative JS (http://www.neilmix.com/narrativejs/doc/).
// The following license applies to the Narcissus code:
/*
 * The contents of this file are subject to the GNU GPL 2.
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is the Narcissus JavaScript engine.
 *
 * The Initial Developer of the Original Code is
 * Brendan Eich <brendan@mozilla.org>.
 * Portions created by the Initial Developer are Copyright (C) 2004
 * the Initial Developer. All Rights Reserved.
*/




var Oni = {}; (function() {


////////////////////////////////////////////////////////////////////////
// Helpers

// Binds a function to an object; the function will be executed with
// its 'this' variable set to 'obj':
function bind(f, obj) {
  return function() {
    return f.apply(obj, arguments);
  }
}

// create an array from a function's arguments object, starting at the
// i's parameter
function slice_args(a, /*[opt]*/ i) {
  return Array.prototype.slice.call(a, i);
}

var win;
try {
  win = window;
}
catch(e) {
  // assuming that we're running under jssh
  win = getWindows()[0];
}

// call 'fct' asynchronously
function callAsync(fct) {
  win.setTimeout(fct, 0);
}

function timeout(cont, duration_ms) {
  var id = win.setTimeout(function() { return cont([true, null]);}, duration_ms);
  return function() { win.clearTimeout(id); }
}

function getCurrentTimeMS() { return (new Date).getTime(); }

////////////////////////////////////////////////////////////////////////
// SJS Runtime

function Scheduler(max_chain) {
  this.maxChain = max_chain;
  this.pendingFunctions = [];
  this.scheduled = false;
  this.executing = false;
}
Scheduler.prototype = {};

Scheduler.prototype.schedule = function(fct, append) {
  if (append) {
    this.pendingFunctions.push(fct);
  }
  else {
    this.pendingFunctions.unshift(fct);
  }
    
  if (!this.scheduled) {
    this.scheduled = true;
    callAsync(bind(Scheduler.prototype._next, this));
  }
};

Scheduler.prototype._next = function() {
  this.scheduled = false;
  this.executeChain();
};

Scheduler.prototype.executeChain = function() {
  if (this.executing) return;
  this.executing = true;
  var chain = 0;
  while (this.pendingFunctions.length && ++chain < this.maxChain) {
    (this.pendingFunctions.shift())();
  }

  if (!this.scheduled && this.pendingFunctions.length) {
    this.scheduled = true;
    callAsync(bind(Scheduler.prototype._next, this));
  }
  this.executing = false;
};
  

var globalScheduler = new Scheduler(300);

var ONI_OEN_TOKEN = {};
function markAsOEN(f) {
  f.__isOEN = ONI_OEN_TOKEN;
}
function isOEN(e) {
  return e && (e.__isOEN == ONI_OEN_TOKEN);
}

var ONI_OEN_EXECUTE_TOKEN = {};

function executeOEN(oen, xc, env) {
  if (!isOEN(oen)) oen = OEN_Quote(oen);
  oen(ONI_OEN_EXECUTE_TOKEN, xc, env);
}

var ONI_CALLBYNEED_TOKEN = {};
function markAsCallByNeed(f) {
  f.__isCallByNeed = ONI_CALLBYNEED_TOKEN;
}
function isCallByNeed(e) {
  return e && (e.__isCallByNeed == ONI_CALLBYNEED_TOKEN);
}

var ONI_OAN_TOKEN = {};
function markAsOAN(f) {
  f.__isOEN = ONI_OEN_TOKEN;
  f.__isOAN = ONI_OAN_TOKEN;
}
function isOAN(e) {
  return e && (e.__isOAN == ONI_OAN_TOKEN);
}

var ONI_OAN_FAPPLY_TOKEN = {};

function fapplyOAN(oan, xc, env, pars, base_obj) {
  if (!isOAN(oan)) {
    oan = OAN_SLift(oan);
  }
  oan(ONI_OAN_FAPPLY_TOKEN, xc, env, pars, base_obj)
}

function OEN_Seq(exps) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Seq(exps, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Alt(exps) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Alt(exps, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Quote(datum) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Quote(datum, arguments[1]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Apply(fexp, args) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Apply(fexp, args, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OAN_ALift(async_f, abort_f) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Quote(OAN_ALift(async_f), arguments[1]);
    }
    else if (arguments[0] == ONI_OAN_FAPPLY_TOKEN) {
      return new OXN_ALift_Apply(async_f, abort_f, arguments[1], arguments[2], arguments[3], arguments[4]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOAN(f);
  return f;
}

function OAN_SLift(sync_f) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Quote(OAN_SLift(sync_f), arguments[1]);
    }
    else if (arguments[0] == ONI_OAN_FAPPLY_TOKEN) {
      var async_f = function(/*cont, arg1, arg2, ... */) {
        var cont = arguments[0];
        var pars = slice_args(arguments, 1);
        var base = this;
        try { var rv;
              if (sync_f.apply) {
                rv = sync_f.apply(base, pars);
              }
              else {
                var command = "sync_f(";
                for (var i=0; i<pars.length; ++i) {
                  if (i!=0) command += ",";
                  command += "pars["+i+"]";
                }
                command += ")";
                rv = eval(command);
              }
              cont([true, rv], true); 
            }
        catch (e) { cont([false, e], true); }
      };
      return new OXN_ALift_Apply(async_f, null, arguments[1], arguments[2], arguments[3], arguments[4]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOAN(f);
  return f;
}

function OEN_Let(bindings, body_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Let(bindings, body_exp, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Get(var_name) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Get(var_name, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Set(lval_exp, value_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Set(lval_exp, value_exp, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_ObjRef(baseobj_exp, identifier_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_ObjRef(baseobj_exp, identifier_exp,
                            arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_CreateBindings(varname_array) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_CreateBindings(varname_array,
                                    arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_This() {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_This(arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OAN_Closure(formals, body_exp, env) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Quote(OAN_Closure(formals, body_exp, env),
                           arguments[1]);
    }
    else if (arguments[0] == ONI_OAN_FAPPLY_TOKEN) {
      var new_env = new OENV(env);
      new_env.thisObject = arguments[4];
      var args = arguments[3];
      for (var i=0; i< formals.length; ++i) {
        new_env.createBinding(formals[i], args[i]);
      }
      return executeOEN(body_exp, arguments[1], new_env);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return void Eval(Apply.apply(this, aargs), this);
    }
  };
  markAsOAN(f);
  return f;
}

function OEN_Lambda(formals, body_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Lambda(formals, body_exp, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Throw(tag_exp, val_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Throw(tag_exp, val_exp, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Catch(tag_exp, body_exp, handler_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Catch(tag_exp, body_exp, handler_exp,
                           arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_If(test_exp, consequent_exp, alternative_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_If(test_exp, consequent_exp, alternative_exp,
                        arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Complete(body_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Complete(body_exp, arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function OEN_Bracket(acquire_exp, use_exp, release_exp) {
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      return new OXN_Bracket(acquire_exp, use_exp, release_exp,
                             arguments[1], arguments[2]);
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  return f;
}

function fork(env, next, expr) {
  var xc = {  next    : next,
              current : null
           };
  executeOEN(expr, xc, env);
  return xc;
}

function OENV(parent, bindings) {
  this.parent = parent;
  if (!bindings) bindings = {};
  this.bindings = bindings;
  if (parent) {
    this.thisObject = parent.thisObject;
    this.rootObject = parent.rootObject;
  }
  else {
    this.thisObject = bindings;
    this.rootObject = bindings;
  }
}
OENV.prototype = {
  createBinding : function(name, val) { this.bindings[name] = val; },
  setBinding : function(name, val) {
    var p = this;
    do {
      if (!p.parent || p.bindings.hasOwnProperty(name)) {
        p.bindings[name] = val;
        return;
      }
    } while((p = p.parent) != null); 
  },
  getBinding : function(name) {
    if (!this.parent || this.bindings.hasOwnProperty(name))
      return this.bindings[name];
    else
      return this.parent.getBinding(name);
  }
  ,
  getThisObject : function() { return this.thisObject; },
  getRootObject : function() { return this.rootObject; }
};

function ORV(value) {
  this.value = value;
}
ORV.prototype = {
  didThrow : function() { return isOniException(this.value); }
};

function OXX(tag, value) {
  this.tag = tag;
  this.value = value;
}
OXX.prototype = { __isOXX : true };

function isOniException(e) {
  return e && (e.__isOXX == true);
}

function OXN(classname) {
  this.oxn_classname = classname;
}
OXN.prototype = {
  __isOXN: true,
  toString: function() { return "OXN<"+this.oxn_classname+">"; }
};

function OXN_Seq(exps, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;
  
  this.exps = exps;
  
  this.next = this;
  this.current = null;
  
  this.i_exp = -1;
  this.exp_count = this.exps.length;
  var me = this;
  globalScheduler.schedule(function() { me.cont(me, new ORV(null)); });
}
OXN_Seq.prototype = new OXN("Seq");

OXN_Seq.prototype.cont = function(exiting_xc, rv) {
  if (this.aborted) {
    this.xc.next.cont(this.xc, new ORV(undefined));
    this.clear();
    return;
  }
  
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  var i = ++this.i_exp;
  if (i >= this.exp_count) {
    this.xc.next.cont(this.xc, rv);
    this.clear();
  }
  else if (i+1 == this.exp_count) {
    executeOEN(this.exps[i], this.xc, this.env);
    this.clear();
  }
  else {
    executeOEN(this.exps[i], this, this.env);
  }
};

OXN_Seq.prototype.abort = function() {
  this.aborted = true;
  if (this.current) {
    this.current.abort();
  }
};

OXN_Seq.prototype.clear = function() {
  delete this.rv;
  delete this.xc;
  delete this.env;
  delete this.current;
};

function OXN_Alt(exps, xc, env) {
  this.xc = xc;
  this.xc.current = this;

  this.fork_count = exps.length;
  this.forks = [];

  for (var i=exps.length-1; i>=0; --i) {
    this.forks.push(fork(env, this, exps[i]));
  }
}
OXN_Alt.prototype = new OXN("Alt");

OXN_Alt.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  if (this.fork_count == this.forks.length) {
    for (var i=0; i<this.forks.length; ++i) {
      if (this.forks[i] == exiting_context) {
        this.rv = rv;
        this.forks[i].current = null;
      }
      else {
        this.forks[i].current.abort();
      }
    }
  }
  else {
    for (var i=0; i<this.forks.length; ++i)
      if (this.forks[i] == exiting_context) {
        this.forks[i].current = null;
        break;
      }
  }

  if (--this.fork_count == 0) {
    this.xc.next.cont(this.xc, this.rv);
    this.clear();
  }
};

OXN_Alt.prototype.abort = function() {
  if (this.forks) {
    for (var i=0; i<this.forks.length; ++i) {
      if (this.forks[i].current)
        this.forks[i].current.abort();
    }
  }
};

OXN_Alt.prototype.clear = function() {
  delete this.xc;
  delete this.forks;
};

function OXN_ExceptionRoot(xc) {
  this.xc = xc;
  this.xc.current = this;
}
OXN_ExceptionRoot.prototype = new OXN("ExceptionRoot");

OXN_ExceptionRoot.prototype.cont = function() {
  this.xc.next.cont(this.xc, new ORV(undefined));
  delete this.xc;
}

OXN_ExceptionRoot.prototype.abort = function() {
  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}

function OXN_Quote(datum, xc) {
  this.xc = xc;
  this.xc.current = this;
  
  this.datum = datum;
  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}
OXN_Quote.prototype = new OXN("Quote");

OXN_Quote.prototype.cont = function() {
  this.xc.next.cont(this.xc, new ORV(this.datum));
  this.clear();
};

OXN_Quote.prototype.abort = function() {
  this.datum = undefined;
};

OXN_Quote.prototype.clear = function() {
  if (!this.xc) return;
  delete this.xc;
  delete this.datum;
};

function OXN_Apply(fexp, aexps, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;
  
  this.fork_count = 1 + aexps.length;
  this.forks = [];
  this.forks.push(fork(env, this, fexp));
  
  for (var i=aexps.length-1; i>=0; --i) {
    this.forks.push(fork(env, this, aexps[i]));
    }
}
OXN_Apply.prototype = new OXN("Apply");

OXN_Apply.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  for (var i=0; i<this.forks.length; ++i)
    if (this.forks[i] == exiting_context) {
      this.forks[i].current = null;
      this.forks[i].rv = rv;
      break;
    }
  
  if (--this.fork_count == 0) {
    if (this.aborted) {
      this.xc.next.cont(this.xc, new ORV(undefined));
      this.clear();
      return;
    }
    
    var oan_rv = this.forks.shift().rv;
    var pars = [];
    for (var i=this.forks.length-1; i>=0; --i) {
      pars.push(this.forks[i].rv.value);
    }
    
     fapplyOAN(oan_rv.value, this.xc, this.env, pars,
              oan_rv.isReference ? oan_rv.base : this.env.getRootObject());
      this.clear();
  }
};

OXN_Apply.prototype.abort = function() {
  if (this.forks) {
    this.aborted = true;
    for (var i=0; i<this.forks.length; ++i) {
      if (this.forks[i].current)
        this.forks[i].current.abort();
    }
  }
};

OXN_Apply.prototype.clear = function() {
  delete this.xc;
  delete this.env;
  delete this.forks;
};
  
function OXN_ALift_Apply(async_f, abort_f, xc, env, args, this_object) {
  this.xc = xc;
  this.xc.current = this;

  var pars = [bind(this.cont, this)];
  pars = pars.concat(args);
  this.this_object = this_object;
  this.abort_f = async_f.apply(this_object, pars);
  if (abort_f) {
    this.abort_f = abort_f;
  }
}
OXN_ALift_Apply.prototype = new OXN("ALift_Apply");

OXN_ALift_Apply.prototype.abort = function() {
  if (this.abort_f) {
    this.abort_f.apply(this.this_object);
    delete this.abort_f;
  }
  this.aborted = true;
  
  this.cont();
};

OXN_ALift_Apply.prototype.cont = function(rv, synchronous) {
  if (this.aborted && !this.xc) {
    return;
  }
  var me = this;
  globalScheduler.schedule(function() { me.cont_inner(rv); }, synchronous != true);
};
  
OXN_ALift_Apply.prototype.cont_inner = function(rv) {
  if (this.aborted) {
    if (!this.xc) {
      return;
    }
    rv = new ORV(undefined);
  }
  else {
    if (rv[0] == true)
      rv = new ORV(rv[1]);
    else {
      new OXN_ExceptionRoot(this.xc);
      rv = new ORV(new OXX("error", rv[1]));
    }
  }
  
  this.xc.next.cont(this.xc, rv);
  delete this.xc;
  delete this.abort_f;
  delete this.this_object;
};

function OXN_Let(bindings, body_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = new OENV(env);
  
  this.body_exp = body_exp;
  
  this.fork_count = 0;
  this.forks = [];
  for (b in bindings) {
    ++this.fork_count;
    this.forks.push([b, fork(this.env, this, bindings[b])]);
  }   
}
OXN_Let.prototype = new OXN("Let");

OXN_Let.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  for (var i=0; i<this.forks.length; ++i) {
    if (this.forks[i][1] == exiting_context) {
      this.env.createBinding(this.forks[i][0], rv.value);
      this.forks[i][1].current = null;
      break;
    }
  }

  if (--this.fork_count == 0) {
    if (this.aborted) {
      this.xc.next.cont(this.xc, new ORV(undefined));
    }
    else {
      executeOEN(this.body_exp, this.xc, this.env);
    }
    this.clear();
  }
};

OXN_Let.prototype.abort = function() {
  if (this.forks) {
    this.aborted = true;
    for (var i=0; i<this.forks.length; ++i) {
      if (this.forks[i][1].current)
        this.forks[i][1].current.abort();
    }
  }
};

OXN_Let.prototype.clear = function() {
  delete this.xc;
  delete this.env;
  delete this.forks;
};

function OXN_Get(var_name, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;
  
  this.var_name = var_name;
  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}
OXN_Get.prototype = new OXN("Get");

OXN_Get.prototype.cont = function() {
  if (this.aborted) {
    this.xc.next.cont(this.xc, new ORV(undefined));
  }
  else {
    this.xc.next.cont(this.xc, new ORV(this.env.getBinding(this.var_name)));
  }
  this.clear();
};

OXN_Get.prototype.abort = function() {
  this.aborted = true;
};

OXN_Get.prototype.clear = function() {
  if (!this.xc) return;
  delete this.xc;
  delete this.env;
  delete this.var_name;
};

function OXN_Set(lval_exp, value_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;

  this.env = env;
  
  this.lval_xc = fork(env, this, lval_exp);
  this.value_xc = fork(env, this, value_exp);
}
OXN_Set.prototype = new OXN("Set");

OXN_Set.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  exiting_context.current = null;
  exiting_context.rv = rv;

  if (this.lval_xc.current == null && this.value_xc.current == null) {
    if (this.lval_xc.rv.isReference) {
      this.lval_xc.rv.base[this.lval_xc.rv.id] = this.value_xc.rv.value;
    }
    else {
      this.env.setBinding(this.lval_xc.rv.value, this.value_xc.rv.value);
    }
    this.xc.next.cont(this.xc, this.value_xc.rv);
    delete this.xc;
    delete this.env;
    delete this.lval_xc;
    delete this.value_xc;
  }
};

OXN_Set.prototype.abort = function() {
  if (!this.lval_xc) return;
  if (this.lval_xc.current)
    this.lval_xc.current.abort();
  if (this.value_xc.current)
    this.value_xc.current.abort();
};

function OXN_ObjRef(baseobj_exp, identifier_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  
  this.base_xc = fork(env, this, baseobj_exp);
  this.id_xc = fork(env, this, identifier_exp);
}
OXN_ObjRef.prototype = new OXN("ObjRef");

OXN_ObjRef.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  exiting_context.current = null;
  exiting_context.rv = rv;

  if (this.base_xc.current == null && this.id_xc.current == null) {
    if (!this.base_xc.rv.value)
      rv = new ORV(undefined); 
    else {
      rv = new ORV(this.base_xc.rv.value[this.id_xc.rv.value]);
      rv.isReference = true;
      rv.base = this.base_xc.rv.value;
      rv.id = this.id_xc.rv.value;
    }
    this.xc.next.cont(this.xc, rv);
    delete this.xc;
    delete this.base_xc;
    delete this.id_xc;
  }
};

OXN_ObjRef.prototype.abort = function() {
  if (!this.base_xc) return;
  if (this.base_xc.current)
    this.base_xc.current.abort();
  if (this.id_xc.current)
    this.id_xc.current.abort();
};    

function OXN_CreateBindings(varname_array, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;

  this.varname_array = varname_array;
  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}
OXN_CreateBindings.prototype = new OXN("CreateBindings");

OXN_CreateBindings.prototype.cont = function() {
  if (!this.aborted) {
    for (var i=0; i<this.varname_array.length; ++i)
      this.env.createBinding(this.varname_array[i], undefined);
  }
  this.xc.next.cont(this.xc, new ORV(undefined));
  delete this.xc;
  delete this.env;
  delete this.varname_array;
};

OXN_CreateBindings.prototype.abort = function() {
  this.aborted = true;
};    


function OXN_This(xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;

  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}
OXN_This.prototype = new OXN("This");

OXN_This.prototype.cont = function() {
  if (this.aborted) {
    this.xc.next.cont(this.xc, new ORV(undefined));
  }
  else {
    this.xc.next.cont(this.xc, new ORV(this.env.getThisObject()));
  }
  delete this.xc;
  delete this.env;
};

OXN_This.prototype.abort = function() {
  this.aborted = true;
};    

function OXN_Lambda(formals, body_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  
  this.closure = OAN_Closure(formals, body_exp, env);
  var cont = bind(this.cont, this);
  globalScheduler.schedule(cont);
}
OXN_Lambda.prototype = new OXN("Lambda");

OXN_Lambda.prototype.cont = function() {
  this.xc.next.cont(this.xc, new ORV(this.closure));
  this.clear();
};

OXN_Lambda.prototype.abort = function() {
  this.closure = undefined;
}

OXN_Lambda.prototype.clear = function() {
  if (!this.xc) return;
  delete this.xc;
  delete this.closure;
};

function OXN_Throw(tag_exp, val_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  
  this.fork_count = 2;
  this.forks = [];
  this.forks.push(fork(env, this, tag_exp));
  this.forks.push(fork(env, this, val_exp));
}
OXN_Throw.prototype = new OXN("Throw");

OXN_Throw.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.xc.next.cont(this.xc, rv);
    return;
  }

  for (var i=0; i<this.forks.length; ++i)
    if (this.forks[i] == exiting_context) {
      this.forks[i].current = null;
      this.forks[i].rv = rv;
      break;
    }

  if (--this.fork_count == 0) {
    if (this.aborted) {
      this.xc.next.cont(this.xc, new ORV(undefined));
    }
    else {
      new OXN_ExceptionRoot(this.xc);
      this.xc.next.cont(this.xc,
                        new ORV(new OXX(this.forks[0].rv.value,
                                        this.forks[1].rv.value)));
    }
    this.clear();
  }
};

OXN_Throw.prototype.abort = function() {
  if (this.forks) {
    this.aborted = true;
    for (var i=0; i<this.forks.length; ++i) {
      if (this.forks[i].current)
        this.forks[i].current.abort();
    }
  }
};

OXN_Throw.prototype.clear = function() {
  delete this.xc;
  delete this.forks;
};

function OXN_Catch(tag_exp, body_exp, handler_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;
  
  this.body_exp = body_exp;
  this.handler_exp = handler_exp;
  this.pending_exception = null;
  
  this.next = this;
  this.current = null;

  executeOEN(tag_exp, this, this.env);
}
OXN_Catch.prototype = new OXN("Catch");

OXN_Catch.prototype.cont = function(exiting_context, rv) {
  if (this.aborted) {
    this.xc.next.cont(this.xc, new ORV(undefined));
    this.clear();
    return;
  }
  
  if (this.body_exp !== undefined) {
    if (rv.didThrow()) {
      this.xc.next.cont(this.xc, rv);
      return;
    }
    this.tag = rv.value;
    executeOEN(this.body_exp, this, this.env);
    delete this.body_exp;
  }
  else if (this.pending_handler) {
    if (rv.didThrow()) {
      this.xc.next.cont(this.xc, rv);
      return;
    }
    fapplyOAN(rv.value, this.xc, this.env, [this.pending_exception.value],
              rv.isReference ? rv.base : this.env.getRootObject());
    this.clear();
  }
  else if (this.pending_exception) {
    if (this.handler_exp !== undefined) {
      executeOEN(this.handler_exp, this, this.env);
      this.pending_handler = true;
      delete this.handler_exp;
    }
    else {
      this.xc.next.cont(this.xc, new ORV(this.pending_exception.value));
      this.clear();
    }
  }
  else {
    if (rv.didThrow()) {
      if (rv.value.tag != this.tag) {
        this.xc.next.cont(this.xc, rv);
        return;
      }

      this.current.abort();
      this.current_aborted = true; 
      this.pending_exception = rv.value;
    }
    else {
      this.xc.next.cont(this.xc, rv);
      this.clear();
    }
  }
};

OXN_Catch.prototype.abort = function() {
  if (this.current) {
    this.aborted = true;
    if (!this.current_aborted)
      this.current.abort();
  }
};

OXN_Catch.prototype.clear = function() {
  delete this.xc;
  delete this.env;
  delete this.current;
  delete this.body_exp;
  delete this.handler_exp;
  delete this.pending_exception;
  delete this.tag;
};

function OXN_If(test_exp, consequent_exp, alternative_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;
  this.env = env;
  
  this.consequent_exp = consequent_exp;
  this.alternative_exp = alternative_exp;
  
  this.next = this;
  this.current = null;

  executeOEN(test_exp, this, this.env);
}
OXN_If.prototype = new OXN("If");

OXN_If.prototype.cont = function(exiting_context, rv) {
  if (this.aborted) {
    this.xc.next.cont(this.xc, new ORV(undefined));
  }
  else {
    if (rv.didThrow()) {
      this.xc.next.cont(this.xc, rv);
      return;
    }

    if (rv.value && this.consequent_exp !== undefined) {
      executeOEN(this.consequent_exp, this.xc, this.env);
    }
    else if (!rv.value && this.alternative_exp !== undefined) {
      executeOEN(this.alternative_exp, this.xc, this.env);
    }
    else {
      this.xc.next.cont(this.xc, rv);
    }
  }
  this.clear();
};

OXN_If.prototype.abort = function() {
  if (this.current) {
    this.aborted = true;
    this.current.abort();
  }
};

OXN_If.prototype.clear = function() {
  delete this.xc;
  delete this.env;
  delete this.current;
};

function OXN_Complete(body_exp, xc, env) {
  this.xc = xc;
  this.xc.current = this;

  this.next = this;
  this.current = null;

  executeOEN(body_exp, this, env);
}
OXN_Complete.prototype = new OXN("Complete");

OXN_Complete.prototype.cont = function(exiting_context, rv) {
  if (rv.didThrow()) {
    this.current.abort();
    if (!this.aborted) {
      this.xc.next.cont(this.xc, rv);
    }
  }
  else {
    this.xc.next.cont(this.xc, this.aborted ? new ORV(undefined) : rv);
    delete this.xc;
    delete this.current;
  }
};

OXN_Complete.prototype.abort = function() {
  this.aborted = true;
};

function OXN_Bracket(acquire_exp, use_exp, release_exp, xc, env) {
  this.xc = xc;
  this.env = env;
  this.xc.current = this;
  this.next = this;
  this.current = null;

  this.use_exp = use_exp;
  this.release_exp = release_exp;

  executeOEN(acquire_exp, this, this.env);
}
OXN_Bracket.prototype = new OXN("Bracket");

OXN_Bracket.prototype.cont = function(exiting_context, rv) {
  if (this.use_exp !== undefined) {
    if (rv.didThrow()) {
      this.thrown = true;
      this.current.abort();
      if (!this.aborted) {
        this.xc.next.cont(this.xc, rv);
      }
    }
    else {
      if (this.thrown) {
        this.xc.next.cont(this.xc, this.aborted ? new ORV(undefined) : rv);
        this.clear();
      }
      else {
        executeOEN(this.use_exp, this, this.env);
        delete this.use_exp;
      }
    }
  }
  else if (this.release_exp !== undefined) {
    if (rv.didThrow()) {
      this.xc.next.cont(this.xc, rv);
    }
    else {
      this.rv = rv;
      executeOEN(this.release_exp, this, this.env);
      delete this.release_exp;
    }
  }
  else {
    if (rv.didThrow()) {
      this.thrown = true;
      this.current.abort();
      if (!this.aborted) {
        this.xc.next.cont(this.xc, rv);
      }
    }
    else {
      this.xc.next.cont(this.xc, this.aborted ? new ORV(undefined) : this.rv);
      this.clear();
    }
  }
};

OXN_Bracket.prototype.abort = function() {
  this.aborted = true;
  if (this.use_exp === undefined && this.release_exp !== undefined) {
    this.current.abort();
  }
};

OXN_Bracket.prototype.clear = function() {
  delete this.xc;
  delete this.env;
  delete this.current;
  delete this.acquire_exp;
  delete this.use_exp;
  delete this.release_exp;
};

function OVE_GenericValue(valueobj) {
  var pendingOXNs = [];
  var readScheduled = false;

  function read() {
    readScheduled = false;
    if (!valueobj.isValueAvailable) {
      return;
    }
    var l = pendingOXNs;
    pendingOXNs = [];
    for (var i=0; i<l.length; ++i)
      if (!l[i].aborted)
        l[i].cont(valueobj.value);
  }
  
  valueobj.valueAvailable = function() {
    if (pendingOXNs.length && !readScheduled) {
      readScheduled = true;
      globalScheduler.schedule(read);
    }
  };
  
  var f = function() {
    if (arguments[0] == ONI_OEN_EXECUTE_TOKEN) {
      var oxn = new OXN_GenericValue(arguments[1]);
      pendingOXNs.push(oxn);
      if (!readScheduled) {
        if (valueobj.isValueAvailable) {
          readScheduled = true;
          globalScheduler.schedule(read);
        }
        else {
          valueobj.forceValue();
        }
      }
      return oxn;
    }
    else {
      var aargs = slice_args(arguments, 0);
      aargs.unshift(f);
      return Apply.apply(this, aargs);
    }
  };
  markAsOEN(f);
  markAsCallByNeed(f);
  return f;
}

function OXN_GenericValue(xc) {
  this.xc = xc;
  this.xc.current = this;
}
OXN_GenericValue.prototype = new OXN("GenericValue");

OXN_GenericValue.prototype.cont = function(rv) {
  this.xc.next.cont(this.xc, rv);
  delete this.xc;
};

OXN_GenericValue.prototype.abort = function() {
  this.aborted = true;
};

function Eval(oen, bindings) {
  var valueObject = {};
  
  valueObject.forceValue = function() {
  };

  valueObject.isValueAvailable = false;
  
  valueObject.setValue = function(val) {
    this.value = val;
    this.isValueAvailable = true;
    this.valueAvailable();
  };
  
  valueObject.cont = function(exiting_context, rv) {
    if (rv.didThrow()) {
      exiting_context.current.abort();
      this.setValue(new ORV(new OXX("nested", rv.value)));
      callAsync(function() { throw "Uncaught Oni exception: '"+rv.value.tag+"', val:'"+rv.value.value+"'";  });
    }
    else {
      this.setValue(rv);
    }
    delete this.current;
  };
  
  valueObject.abort = function() {
    if (this.current) {
      this.current.abort();
    }
  };

  valueObject.current =  null;

  valueObject.next = valueObject;

  var ove = OVE_GenericValue(valueObject);
 
  executeOEN(oen, valueObject, new OENV(null, bindings));
  
  globalScheduler.executeChain();
  return ove;
};
this["Eval"] = Eval;

function Seq(/* exp1, exp2, ... */) {
  return OEN_Seq(arguments);
}
this["Seq"] = Seq;

function Alt(/* exp1, exp2, ... */) {
  return OEN_Alt(arguments);
}
this["Alt"] = Alt;

var Quote = OEN_Quote; 
this["Quote"] = Quote;

function Apply(/* fexp, aexp1, aexp2, ... */) {
  return OEN_Apply(arguments[0], slice_args(arguments, 1));
}
this["Apply"] = Apply;

function If(/* test_exp, consequent_exp, alternative_exp? */) {
  return OEN_If(arguments[0], arguments[1], arguments[2]);
}
this["If"] = If;

function Complete(/* exp+ */) {
  var exp = slice_args(arguments, 0);
  if (exp.length == 1)
    exp = exp[0];
  else
    exp = Seq.apply(this, exp);
  
  return OEN_Complete(exp);
}
this["Complete"] = Complete;

var Bracket = OEN_Bracket;
this["Bracket"] = Bracket;

function Let(/* bindings, exp+ */) {
  var bindings = arguments[0];
  var exp = slice_args(arguments, 1);
  if (exp.length == 1)
    exp = exp[0];
  else
    exp = Seq.apply(this, exp);
  
  return OEN_Let(bindings, exp);
}
this["Let"] = Let;

var Get = OEN_Get;
this["Get"] = Get;

var Set = OEN_Set; 
this["Set"] = Set;

var ObjRef = OEN_ObjRef;
this["ObjRef"] = ObjRef;

var CreateBindings = OEN_CreateBindings;
this["CreateBindings"] = CreateBindings;

var This = OEN_This;
this["This"] = This;

function Throw(tag, val_exp) {
  return OEN_Throw(Quote(tag), val_exp);
};
this["Throw"] = Throw;

function Catch(/*tag_handler, exp*/) {
  var tag_handler = arguments[0];
  var body_exp = slice_args(arguments, 1);
  if (body_exp.length == 1)
    body_exp = body_exp[0];
  else
    body_exp = Seq.apply(this, body_exp);
  
  return OEN_Catch(Quote(tag_handler[0]),
                   body_exp,
                   tag_handler[1] ? tag_handler[1] : undefined);
};
this["Catch"] = Catch;

var tag_Break = {};
var tag_Continue = {};
function Loop(/*exp+*/) {
  var exp = slice_args(arguments, 0);
  if (exp.length == 1)
    exp = exp[0];
  else
    exp = Seq.apply(this, exp);
  
  return Catch([tag_Break],
               Let({ "__loop__" : Lambda([],
                                         Catch([tag_Continue], exp),
                                         ALift(function(c){ c([true,1]); })(),
                                         Get("__loop__")() )
                   },
                   Get("__loop__")()));
}
function Break(exp) {
  return Throw(tag_Break, exp);
}
function Continue() {
  return Throw(tag_Continue);
}
this["Loop"] = Loop;
this["Break"] = Break;
this["Continue"] = Continue;
this["tag_Continue"] = tag_Continue
this["tag_Break"] = tag_Break

var ALift = OAN_ALift;
this["ALift"] = ALift;

var SLift = OAN_SLift;
this["SLift"] = SLift;

function Lambda(/* formals, exp+ */) {
  var formals = arguments[0];
  var body_exp = slice_args(arguments, 1);
  if (body_exp.length == 1)
    body_exp = body_exp[0];
  else
    body_exp = Seq.apply(this, body_exp);

  return OEN_Lambda(formals, body_exp);
}
this["Lambda"] = Lambda;

function Defun(/* formals, exp+ */) {
  var formals = arguments[0];
  var body_exp = slice_args(arguments, 1);
  if (body_exp.length == 1)
    body_exp = body_exp[0];
  else
    body_exp = Seq.apply(this, body_exp);
  
  return OAN_Closure(formals, body_exp, {});
}
this["Defun"] = Defun;

var Nop = SLift(function() { return null; });
this["Nop"] = Nop;

var Stop = ALift(function() { /* continuation never called */ });
this["Stop"] = Stop;

var Par = Nop;
this["Par"] = Par;

this['||'] = SLift(function(a,b) { return a || b; });;
this['&&'] = SLift(function(a,b) { return a && b; });;
this['|'] = SLift(function(a,b) { return a | b; });;
this['^'] = SLift(function(a,b) { return a ^ b; });;
this['&'] = SLift(function(a,b) { return a & b; });;
this['==='] = SLift(function(a,b) { return a === b; });;
this['=='] = SLift(function(a,b) { return a == b; });;
this['!=='] = SLift(function(a,b) { return a !== b; });;
this['!='] = SLift(function(a,b) { return a != b; });;
this['<<'] = SLift(function(a,b) { return a << b; });;
this['<='] = SLift(function(a,b) { return a <= b; });;
this['<'] = SLift(function(a,b) { return a < b; });;
this['>>>'] = SLift(function(a,b) { return a >>> b; });;
this['>>'] = SLift(function(a,b) { return a >> b; });;
this['>='] = SLift(function(a,b) { return a >= b; });;
this['>'] = SLift(function(a,b) { return a > b; });;
this['+'] = SLift(function(a,b) { return a + b; });;
this['-'] = SLift(function(a,b) { return a - b; });;
this['*'] = SLift(function(a,b) { return a * b; });;
this['/'] = SLift(function(a,b) { return a / b; });;
this['%'] = SLift(function(a,b) { return a % b; });;
this['u_'+'!'] = SLift(function(a) { return ! a; });;
this['u_'+'~'] = SLift(function(a) { return ~ a; });;
this['u_'+'+'] = SLift(function(a) { return + a; });;
this['u_'+'-'] = SLift(function(a) { return - a; });;

var New = SLift(function(ctor, args) {
    return new ctor();
});
this["New"] = New;

var NewWithArgs = SLift(function() {
  var pars = slice_args(arguments, 0);
  var command = "new pars[0] (";
  for (var i=1; i < pars.length; ++i) {
    if (i != 1) command += ",";
    command += "pars["+i+"]";
  }
  command += ")";
  return eval(command);
});
this["NewWithArgs"] = NewWithArgs;

var Typeof = SLift(function(o) { return typeof o; });
this["Typeof"] = Typeof;

var Not = SLift(function(a) { return !a; });
this["Not"] = Not;

var Equals = SLift(function(a, b) { return a == b; });
this["Equals"] = Equals;

var NEquals = SLift(function(a, b) { return a != b; });
this["NEquals"] = NEquals;

var IsNull = SLift(function(obj) { return !obj || (obj.length === 0); });
this["IsNull"] = IsNull;

var Obj = SLift(function(/* path1, value1, ..., path_n, value_n */) {
  var obj = {};
  for (var i=0; i+1<arguments.length; i+=2) {
    var path = arguments[i];
    var ref = obj;
    if (path instanceof Array) {
      for (var e = 0; e<path.length-1; ++e) {
        if (!ref[path[e]]) ref[path[e]] = {};
        ref = ref[path[e]];
      }
      path = path[e];
    }
    if (ref[path]) throw("Duplicate member '"+path+"' in JSON Obj");
    ref[path] = arguments[i+1];
  }
  
  return obj;
});
this["Obj"] = Obj;

var ObjMem = SLift(function(obj /*, member1, member2, ... */) {
  var rv = obj;
  for (var i=1; i<arguments.length; ++i) {
    rv = rv[arguments[i]];
  }
  return rv;
});
this["ObjMem"] = ObjMem;

var emptylist = [];

var Car = SLift(function(lst) { return lst[0]; });
this["Car"] = Car;

var Cdr = SLift(function(lst) { return lst.length > 1 ? lst.slice(1) : emptylist; });
this["Cdr"] = Cdr;

var Cadr = SLift(function(lst) { return lst[1]; });
this["Cadr"] = Cadr;

var Caddr = SLift(function(lst) { return lst[2]; });
this["Caddr"] = Caddr;

var Cadddr = SLift(function(lst) { return lst[3]; });
this["Cadddr"] = Cadddr;

var ListRef = SLift(function(lst, i) { return lst[i]; });
this["ListRef"] = ListRef;

var ListTail = SLift(function(lst, i) { return lst.length > i ? lst.slice(i) : emptylist; });
this["ListTail"] = ListTail;

var Member = SLift(function(obj, lst) {
  for (var i=0; i<lst.length; ++i) {
    if (lst[i] == obj)
      return lst.slice(i);
  }
  return false;
});
this["Member"] = Member;

var List = SLift(function(/*objs*/) {
  return slice_args(arguments, 0);
});
this["List"] = List;

var Cons = SLift(function(obj, lst) {
  var res = [obj];
  return res.concat(lst);
});
this["Cons"] = Cons;

var Remove = SLift(function(obj, lst) {
  var res = [];
  for (var i=0; i<lst.length; ++i)
    if (lst[i] != obj)
      res.push(lst[i]);
  return res;
});
this["Remove"] = Remove;
  
function GetCar(v) { return Car(Get(v)); }
this["GetCar"] = GetCar;

function GetCdr(v) { return Cdr(Get(v)); }
this["GetCdr"] = GetCdr;

function GetCadr(v) { return Cadr(Get(v)); }
this["GetCadr"] = GetCadr;

function GetCaddr(v) { return Caddr(Get(v)); }
this["GetCaddr"] = GetCaddr;

function GetCadddr(v) { return Cadddr(Get(v)); }
this["GetCadddr"] = GetCadddr;

var Add = SLift(function(a,b) { return a+b; });
this["Add"] = Add;

var Sub = SLift(function(a, b) { return a-b; });
this["Sub"] = Sub;

var Mul = SLift(function(a, b) { return a*b; });
this["Mul"] = Mul;

var Div = SLift(function(a, b) { return a/b; });
this["Div"] = Div;

var Random = SLift(function(ceil) { return Math.random()*ceil; });
this["Random"] = Random;

var Sleep = ALift(timeout);
this["Sleep"] = Sleep;

function Delay(/* duration, exp* */) {
  var duration = arguments[0];
  var exps = slice_args(arguments, 1);
  exps.unshift(Apply(Sleep, duration));
  return Seq.apply(this, exps);
}
this["Delay"] = Delay;


var GetCurrentTimeMS = SLift(getCurrentTimeMS);

function Time(/*exp+*/) {
  var exp = slice_args(arguments, 0);
  if (exp.length == 1)
    exp = exp[0];
  else
    exp = Seq.apply(this, exp);

  return Let({ "__time__" : GetCurrentTimeMS() },
             Let({ "__res__" : exp },
                 List(Get("__res__"), Sub(GetCurrentTimeMS(),
                                          Get("__time__")))));
}
this["Time"] = Time;

function _AtomicVar(value) {
  this.value = value;
}
_AtomicVar.prototype = {};

_AtomicVar.prototype.read = function() { return this.value; };
_AtomicVar.prototype.write = function(value) { this.value = value; };
_AtomicVar.prototype.transform = function(xform_func) { return this.value = xform_func(this.value); };

var AtomicVar = {};
AtomicVar.create = function(value) { return new _AtomicVar(value); };
AtomicVar.Create = SLift(AtomicVar.create);
AtomicVar.Read = SLift(function(v) { return v.read(); });
AtomicVar.Write = SLift(function(v, value) { v.write(value); });
AtomicVar.Transform = SLift(function(v, xform) { return v.transform(xform); });
this["AtomicVar"] = AtomicVar;

function _Signal() {
  this.listeners = [];
}
_Signal.prototype = {};

_Signal.prototype.notify = function(val) {
  var ls = this.listeners;
  this.listeners = [];
  for (var i=0; i<ls.length; ++i) {
    ls[i]([true, val]);
  }
};

_Signal.prototype.wait = function(cont) {
  this.listeners.push(cont);
  var me = this;
  return function() {
    for (var i=0; i<me.listeners.length; ++i) {
      if (me.listeners[i] == cont) {
        me.listeners.splice(i, 1);
        return;
      }
    }
  };
};

var Signal = {};
Signal.create = function() { return new _Signal(); };
Signal.Create = SLift(Signal.create);
Signal.Notify = SLift(function(s, val) { return s.notify(val);});
Signal.Wait = ALift(function(cont, s) { return s.wait(cont); });

this["Signal"] = Signal;

function _Barrier(is_open) {
  this.is_open = is_open ? true : false;
  this.listeners = [];
}
_Barrier.prototype = {};

_Barrier.prototype.open = function() {
  this.is_open = true;
  var ls = this.listeners;
  this.listeners = [];
  for (var i=0; i<ls.length; ++i) {
    ls[i]([true, null]);
  }
};

_Barrier.prototype.close = function() {
  this.is_open = false;
};

_Barrier.prototype.pass = function(cont) {
  if (this.is_open)
    globalScheduler.schedule(function() { cont([true, null]); });
  else {
    this.listeners.push(cont);
    var me = this;
    return function() {
      for (var i=0; i<me.listeners.length; ++i) {
        if (me.listeners[i] == cont) {
          me.listeners.splice(i, 1);
          return;
        }
      }
    };
  }
};

var Barrier = {};
Barrier.create = function(is_open) { return new _Barrier(is_open); };
Barrier.Create = SLift(Barrier.create);
Barrier.Open = SLift(function(b) { return b.open();} );
Barrier.Close = SLift(function(b) { return b.close();});
Barrier.Pass = ALift(function(cont, b) { return b.pass(cont);});
  
this["Barrier"] = Barrier;

function _Channel() {
  this.puts = [];
  this.collects = [];
  this.availBarrier = Barrier.create(false);
  this.emptyBarrier = Barrier.create(true);    
}
_Channel.prototype = {};

_Channel.prototype.put = function(val, cont) {
  this.puts.push({ val: val, cont: cont });
  this.process();
};

_Channel.prototype.collect = function(cont) {
  this.collects.push(cont);
  this.process();
};

_Channel.prototype.process = function() {
  if (this.puts.length && this.collects.length) {
    var p = this.puts.shift();
    var c = this.collects.shift();
    c([true, p.val]);
    if (p.cont)
      p.cont([true,null]);
  }
  
  if (this.puts.length && !this.collects.length)
    this.availBarrier.open();
  else
    this.availBarrier.close();

  if (!this.puts.length)
    this.emptyBarrier.open();
  else
    this.emptyBarrier.close();
};

_Channel.prototype.waitAvail = function(cont) {
  return this.availBarrier.pass(cont);
};

_Channel.prototype.waitEmpty = function(cont) {
  return this.emptyBarrier.pass(cont);
};

var Channel = {};
Channel.create = function() { return new _Channel(); };
Channel.Create = SLift(Channel.create);
Channel.Put = ALift(function(cont, c, val) { return c.put(val, cont);});
Channel.Collect = ALift(function(cont, c) { return c.collect(cont);});
Channel.WaitAvail = ALift(function(cont, c) { return c.waitAvail(cont);}); 
Channel.WaitEmpty = ALift(function(cont, c) { return c.waitEmpty(cont);});

this["Channel"] = Channel;

}).call(Oni);
/*
 Stratified JS compiler v0.3 based on Narcissus
*/

 /*
  * njs edit:
  * - Neil: combine jsdefs.js and jsparse.js into a single file as part of an
  *   effort to reduce namespace pollution.
  * - Neil: make opTypeName order explicit for env compatibility.  The original
  *   source relied on a SpiderMonkey specific behavior where object key
  *   iteration occurs in the same order in which the keys were defined in 
  *   the object.
  * - Neil: perf optimizations for OOM+ parse speedup
  * - Neil: make code x-env-compatible
  * - chocolateboy 2006-06-01: add support for $ in identifiers and remove support for ` as the first character as per:
  *   http://www.mozilla.org/js/language/es4/formal/lexer-semantics.html#N-InitialIdentifierCharacter and
  *   http://www.mozilla.org/js/language/es4/formal/lexer-semantics.html#N-ContinuingIdentifierCharacter
  */

var SJS = {};

(function() {

/*
 * Narcissus - JS implemented in JS.
 *
 * Well-known constants and lookup tables.  Many consts are generated from the
 * tokens table via eval to minimize redundancy, so consumers must be compiled
 * separately to take advantage of the simple switch-case constant propagation
 * done by SpiderMonkey.
 */

// NJS EDIT: remove references to global

	var tokens = [
		// End of source.
		"END",
	  
		// Operators and punctuators.  Some pair-wise order matters, e.g. (+, -)
		// and (UNARY_PLUS, UNARY_MINUS).
		"\n", ";",
		",",
    "@", // Stratified Alt operator
		"=",
		"?", ":", 
		"||",
		"&&",
		"|",
		"^",
		"&",
		"==", "!=", "===", "!==",
		"<", "<=", ">=", ">",
		"<<", ">>", ">>>",
		"+", "-",
		"*", "/", "%",
		"!", "~", "UNARY_PLUS", "UNARY_MINUS",
		"++", "--",
		".",
		"[", "]",
		"{", "}",
		"(", ")",
	  
		// Nonterminal tree node type codes.
		"SCRIPT", "BLOCK", "LABEL", "FOR_IN", "CALL", "NEW_WITH_ARGS", "INDEX",
		"ARRAY_INIT", "OBJECT_INIT", "PROPERTY_INIT", "GETTER", "SETTER",
		"GROUP", "LIST",
	  
		// Terminals.
		"IDENTIFIER", "NUMBER", "STRING", "REGEXP",
	  
		// Keywords.
		"break",
		"case", "catch", "const", "continue",
		"debugger", "default", "delete", "do",
		"else", "enum",
		"false", "finally", "for", "function",
		"if", "in", "instanceof",
		"new", "null",
		"return",
		"switch",
		"this", "throw", "true", "try", "typeof",
		"var", "void",
		"while", "with",

    // Stratified Keywords
    "suspend", "retract"
	];

	// Operator and punctuator mapping from token to tree node type name.
	// NB: superstring tokens (e.g., ++) must come before their substring token
	// counterparts (+ in the example), so that the opRegExp regular expression
	// synthesized from this list makes the longest possible match.
	// NJS EDIT: NB comment above indicates reliance on SpiderMonkey-specific
	//       behavior in the ordering of key iteration -- see EDIT below.
	var opTypeNames = {
		'\n':   "NEWLINE",
		';':    "SEMICOLON",
		',':    "COMMA",
    '@':    "ALT", // Stratified Alt Operator
		'?':    "HOOK",
		':':    "COLON",
		'||':   "OR",
		'&&':   "AND",
		'|':    "BITWISE_OR",
		'^':    "BITWISE_XOR",
		'&':    "BITWISE_AND",
		'===':  "STRICT_EQ",
		'==':   "EQ",
		'=':    "ASSIGN",
		'!==':  "STRICT_NE",
		'!=':   "NE",
		'<<':   "LSH",
		'<=':   "LE",
		'<':    "LT",
		'>>>':  "URSH",
		'>>':   "RSH",
		'>=':   "GE",
		'>':    "GT",
		'++':   "INCREMENT",
		'--':   "DECREMENT",
		'+':    "PLUS",
		'-':    "MINUS",
		'*':    "MUL",
		'/':    "DIV",
		'%':    "MOD",
		'!':    "NOT",
		'~':    "BITWISE_NOT",
		'.':    "DOT",
		'[':    "LEFT_BRACKET",
		']':    "RIGHT_BRACKET",
		'{':    "LEFT_CURLY",
		'}':    "RIGHT_CURLY",
		'(':    "LEFT_PAREN",
		')':    "RIGHT_PAREN"
	};
  
	// NJS EDIT: created separate opTypeOrder array to indicate the order in which
	//           to evaluate opTypeNames.  (Apparently, SpiderMonkey must iterate
	//           hash keys in the order in which they are defined, an implementation
	//           detail which the original narcissus code relied on.)
	var opTypeOrder = [
		'\n',
		';',
		',',
    '@', // Stratified Alt Operator
		'?',
		':',
		'||',
		'&&',
		'|',
		'^',
		'&',
		'===',
		'==',
		'=',
		'!==',
		'!=',
		'<<',
		'<=',
		'<',
		'>>>',
		'>>',
		'>=',
		'>',
		'++',
		'--',
		'+',
		'-',
		'*',
		'/',
		'%',
		'!',
		'~',
		'.',
		'[',
		']',
		'{',
		'}',
		'(',
		')'
	];
  
	// Hash of keyword identifier to tokens index.  NB: we must null __proto__ to
	// avoid toString, etc. namespace pollution.
  // afri: not sure this works x-platform... but we explicitly check the type of
  //       of properties when we access the object. this guards against ns pollution
  //       (at least somewhat)
	var keywords = {__proto__: null};
  
	// Define const END, etc., based on the token names.  Also map name to index.
	// NJS EDIT: use "var " prefix to make definitions local to this function
	var consts = "var ";
	for (var i = 0, j = tokens.length; i < j; i++) {
		if (i > 0)
			consts += ", ";
		var t = tokens[i];
		var name;
		if (/^[a-z]/.test(t)) {
			name = t.toUpperCase();
			keywords[t] = i;
		} else {
			name = (/^\W/.test(t) ? opTypeNames[t] : t);
		}
		consts += name + " = " + i;
		this[name] = i;
		tokens[t] = i;
	}
	eval(consts + ";");
	
	// Map assignment operators to their indexes in the tokens array.
	var assignOps = ['|', '^', '&', '<<', '>>', '>>>', '+', '-', '*', '/', '%'];
	
	for (i = 0, j = assignOps.length; i < j; i++) {
		t = assignOps[i];
		assignOps[t] = tokens[t];
	}
  
  //----------------------------------------------------------------------
  /*
   * Narcissus - JS implemented in JS.
   *
   * Lexical scanner and parser.
   */

  // Build a regexp that recognizes operators and punctuators (except newline).
	// NJS EDIT: change for loop from iterating through opTypeNames keys to using
	//           opTypeOrder array so that we're not dependent on SpiderMonkey's
	//           key order default behavior.
	// NJS EDIT: change regex structure for OOM perf improvement
  var opRegExpSrc = "^(?:";
  for (var i=0; i<opTypeOrder.length;++i) {
    var op = opTypeOrder[i];
    if (op == '\n')
      continue;
    if (opRegExpSrc != "^(?:")
      opRegExpSrc += "|^";
    
		// NJS EDIT: expand out this regexp for environments that don't support $&
		//opRegExpSrc += op.replace(/[?|^&(){}\[\]+\-*\/\.]/g, "\\$&");
		op = op.replace(/\?/g, "\\?");
		op = op.replace(/\|/g, "\\|");
		op = op.replace(/\^/g, "\\^");
		op = op.replace(/\&/g, "\\&");
		op = op.replace(/\(/g, "\\(");
		op = op.replace(/\)/g, "\\)");
		op = op.replace(/\{/g, "\\{");
		op = op.replace(/\}/g, "\\}");
		op = op.replace(/\[/g, "\\[");
		op = op.replace(/\]/g, "\\]");
		op = op.replace(/\+/g, "\\+");
		op = op.replace(/\-/g, "\\-");
		op = op.replace(/\*/g, "\\*");
		op = op.replace(/\//g, "\\/");
		op = op.replace(/\./g, "\\.");
		opRegExpSrc += op;    
  }
  opRegExpSrc += ")";
  var opRegExp = new RegExp(opRegExpSrc);

  // A regexp to match floating point literals (but not integer literals).
	// EDIT: change regex structure for OOM perf improvement
	var fpRegExp = /^(?:\d+\.\d*(?:[eE][-+]?\d+)?|\d+(?:\.\d*)?[eE][-+]?\d+|\.\d+(?:[eE][-+]?\d+)?)/;

  // A regexp to match regexp literals.
  var reRegExp = /^\/((?:\\.|\[(?:\\.|[^\]])*\]|[^\/])+)\/([gimy]*)/;

  function Tokenizer(s, f, l) {
    this.cursor = 0;
    this.source = String(s);
    this.tokens = [];
    this.tokenIndex = 0;
    this.lookahead = 0;
    this.scanNewlines = false;
    this.scanOperand = true;
    this.filename = f || "";
    this.lineno = l || 1;
  }

  Tokenizer.prototype = {
	  // NJS EDIT: change "input" from a getter to a regular method for compatibility
	  //           with older JavaScript versions
	  input: function() {
		  return this.source.substring(this.cursor);
	  },
	 
	  // NJS EDIT: change "done" from a getter to a regular method for compatibility
	  //           with older JavaScript versions
		done: function() {
			return this.peek() == END;
		},
	 
	  // NJS EDIT: change "token" from a getter to a regular method for compatibility
	  //           with older JavaScript versions
		token: function() {
			return this.tokens[this.tokenIndex];
		},

    match: function (tt) {
      return this.get() == tt || this.unget();
    },

    mustMatch: function (tt) {
      if (!this.match(tt))
        throw this.newSyntaxError("Missing " + tokens[tt].toLowerCase());
      // NJS EDIT -> token()
      return this.token();
    },

    peek: function () {
      var tt, next;
      if (this.lookahead) {
        next = this.tokens[(this.tokenIndex + this.lookahead) & 3];
        if (this.scanNewlines && next.lineno != this.lineno)
          tt = NEWLINE;
        else
          tt = next.type;
      } else {
        tt = this.get();
        this.unget();
      }
      return tt;
    },
    
    peekOnSameLine: function () {
        this.scanNewlines = true;
        var tt = this.peek();
        this.scanNewlines = false;
        return tt;
    },

    get: function () {
      var token;
      while (this.lookahead) {
        --this.lookahead;
        this.tokenIndex = (this.tokenIndex + 1) & 3;
        token = this.tokens[this.tokenIndex];
        if (token.type != NEWLINE || this.scanNewlines)
          return token.type;
      }

      for (;;) {
        var input = this.input();
				var firstChar = input.charCodeAt(0);
				// NJS EDIT: check first char, then use regex
				// valid regex whitespace includes char codes: 9 10 11 12 13 32
				if(firstChar == 32 || (firstChar >= 9 && firstChar <= 13)) {
					var match = input.match(this.scanNewlines ? /^[ \t]+/ : /^\s+/); // NJS EDIT: use x-browser regex syntax
          if (match) {
            var spaces = match[0];
            this.cursor += spaces.length;
            var newlines = spaces.match(/\n/g);
            if (newlines)
              this.lineno += newlines.length;
            input = this.input();
          }
        }
        
				// NJS EDIT: improve perf by checking first string char before proceeding to regex,
				//       use x-browser regex syntax
				if (input.charCodeAt(0) != 47 || !(match = input.match(/^\/(?:\*(?:.|\n)*?\*\/|\/.*)/)))
					break;
				var comment = match[0];
				this.cursor += comment.length;
				newlines = comment.match(/\n/g);
				if (newlines)
					this.lineno += newlines.length; // afri: add missing ';'
			}

      this.tokenIndex = (this.tokenIndex + 1) & 3;
      token = this.tokens[this.tokenIndex];
      if (!token)
        this.tokens[this.tokenIndex] = token = {};

      if (!input)
        return token.type = END;

      // NJS EDIT: guard by checking char codes before going to regex
      var firstChar = input.charCodeAt(0);
      
      if ((firstChar == 46 || (firstChar > 47 && firstChar < 58)) &&
          (match = input.match(fpRegExp))) { // NJS EDIT: use x-browser regex syntax
        token.type = NUMBER;
        token.value = parseFloat(match[0]);
      } else if ((firstChar > 47 && firstChar < 58) &&
                 (match = input.match(/^(?:0[xX][\da-fA-F]+|^0[0-7]*|\d+)/))) { // NJS EDIT: change regex structure for OOM perf improvement; use x-browser regex syntax
        token.type = NUMBER;
        token.value = parseInt(match[0]);
      } else if ((match = input.match(/^[$_\w]+/))) {       // FIXME no ES3 unicode, NJS EDIT: use x-browser syntax
        var id = match[0];
        // NJS EDIT: check the type of the value in the keywords hash, as different envs
        //           expose implicit Object properties that SpiderMonkey does not.
        // afri: actually, the real problem is that the __proto__ hack used in
        //       the keywords hash is not x-browser.
        // token.type = keywords[id] || IDENTIFIER;
        token.type = typeof(keywords[id]) == "number" ? keywords[id] : IDENTIFIER;
        token.value = id;
      } else if ((match = input.match(/^"(?:\\.|[^"])*"|^'(?:\\.|[^'])*'/))) { //"){ // NJS EDIT: use x-browser regex syntax
        token.type = STRING;
        token.value = eval(match[0]);
      } else if (this.scanOperand && (match = input.match(reRegExp))) { // NJS EDIT: use x-browser regex syntax
        token.type = REGEXP;
        token.value = new RegExp(match[1], match[2]);
      } else if ((match = input.match(opRegExp))) { // NJS EDIT: use x-browser regex syntax
        var op = match[0];
        // NJS EDIT: IE doesn't support indexing of strings -- use charAt
        if (assignOps[op] && input.charAt(op.length) == '=') {
          token.type = ASSIGN;
          token.assignOp = eval(opTypeNames[op]); // XXX afri - why eval
          match[0] += '=';
        } else {
          token.type = eval(opTypeNames[op]);
          if (this.scanOperand &&
              (token.type == PLUS || token.type == MINUS)) {
            token.type += UNARY_PLUS - PLUS;
          }
          token.assignOp = null;
        }
        token.value = op;
      } else if (this.scanNewlines && (match = input.match(/^\n/))) { // afri: use x-browser regex syntax
        token.type = NEWLINE;
      } else {
          throw this.newSyntaxError("Illegal token");
      }

      token.start = this.cursor;
      this.cursor += match[0].length;
      token.end = this.cursor;
      token.lineno = this.lineno;
      return token.type;
    },

    unget: function () {
      if (++this.lookahead == 4) throw "PANIC: too much lookahead!";
      this.tokenIndex = (this.tokenIndex - 1) & 3;
    },

    newSyntaxError: function (m) {
      var e = new SyntaxError(m, this.filename, this.lineno);
      e.lineNumber = this.lineno; // NJS EDIT: x-browser exception handling
      e.source = this.source;
      e.cursor = this.cursor;
      return e;
    }
  };

  function CompilerContext(inFunction) {
    this.inFunction = inFunction;
    this.stmtStack = [];
    this.funDecls = [];
    this.varDecls = [];
  }

  var CCp = CompilerContext.prototype;
  CCp.bracketLevel = CCp.curlyLevel = CCp.parenLevel = CCp.hookLevel = 0;
  CCp.ecmaStrictMode = CCp.inForLoopInit = false;

  function Script(t, x) {
    var n = Statements(t, x);
    n.type = SCRIPT;
    n.funDecls = x.funDecls;
    n.varDecls = x.varDecls;
    return n;
  }


  // NJS EDIT: change "top" method to be a regular method, rather than defined
  //           via the SpiderMonkey-specific __defineProperty__
  
  // Node extends Array, which we extend slightly with a top-of-stack method.
  Array.prototype.top = function() {
    return this.length && this[this.length-1];
  };

  function Node(t, type) {
    // NJS EDIT: "inherit" from Array in an x-browser way.
    var _this = [];
    for (var n in Node.prototype)
      _this[n] = Node.prototype[n];

    _this.constructor = Node;

    // NJS EDIT: -> token()
    var token = t.token();
    if (token) {
      _this.type = type || token.type;
      _this.value = token.value;
      _this.lineno = token.lineno;
      _this.start = token.start;
      _this.end = token.end;
    } else {
      _this.type = type;
      _this.lineno = t.lineno;
    }
    _this.tokenizer = t;
    
    for (var i = 2; i < arguments.length; i++)
      _this.push(arguments[i]);

    return _this;
  }

  var Np = Node.prototype; // NJS EDIT: don't inherit from array
  Np.toSource = Object.prototype.toSource;

// Always use push to add operands to an expression, to update start and end.
  Np.push = function (kid) {
    if (kid.start < this.start)
      this.start = kid.start;
    if (this.end < kid.end)
      this.end = kid.end;
    //return Array.prototype.push.call(this, kid);
    this[this.length] = kid; // NJS EDIT? x-browser?
  }

  Node.indentLevel = 0;

  function tokenstr(tt) {
    var t = tokens[tt];
    return /^\W/.test(t) ? opTypeNames[t] : t.toUpperCase();
  }

  Np.toString = function () {
    var a = [];
    for (var i in this) {
      if (this.hasOwnProperty(i) && i != 'type' && i != 'target' && typeof(this[i]) != 'function') // NJS edit: function check, because we "inherit" from Array differently
        a.push({id: i, value: this[i]});
    }
    a.sort(function (a,b) { return (a.id < b.id) ? -1 : 1; });
    var INDENTATION = "  "; // afri: const -> var
    var n = ++Node.indentLevel;
    var s = "{\n" + INDENTATION.repeat(n) + "type: " + tokenstr(this.type);
    for (i = 0; i < a.length; i++)
      s += ",\n" + INDENTATION.repeat(n) + a[i].id + ": " + a[i].value;
    n = --Node.indentLevel;
    s += "\n" + INDENTATION.repeat(n) + "}";
    return s;
  }; // afri: add ';'

  Np.getSource = function () {
    return this.tokenizer.source.slice(this.start, this.end);
  };

	// NJS EDIT: change "filename" method to be a regular method, rather than defined
	//           via the SpiderMonkey-specific __defineGetter__
	Np.filename = function () { return this.tokenizer.filename; };

  // NJS EDIT: don't use __defineProperty__
  String.prototype.repeat = function (n) {
    var s = "", t = this + s;
    while (--n >= 0)
      s += t;
    return s;
  };
  
  // Statement stack and nested statement handler.
  function nest(t, x, node, func, end) {
    x.stmtStack.push(node);
    var n = func(t, x);
    x.stmtStack.pop();
    end && t.mustMatch(end);
    return n;
  }

  function Statements(t, x) {
    // NJS: new Node -> Node
    var n = Node(t, BLOCK);
    x.stmtStack.push(n);
    // NJS: -> done()
    while (!t.done() && t.peek() != RIGHT_CURLY)
      n.push(Statement(t, x));
    x.stmtStack.pop();
    return n;
  }

  function Block(t, x) {
    t.mustMatch(LEFT_CURLY);
    var n = Statements(t, x);
    t.mustMatch(RIGHT_CURLY);
    return n;
  }

  // afri: const -> var
  var DECLARED_FORM = 0, EXPRESSED_FORM = 1, STATEMENT_FORM = 2;

  function Statement(t, x) {
    var i, label, n, n2, ss, tt = t.get();
    
    // Cases for statements ending in a right curly return early, avoiding the
    // common semicolon insertion magic after this switch.
    switch (tt) {
    case FUNCTION:
      return FunctionDefinition(t, x, true,
                                (x.stmtStack.length > 1)
                                ? STATEMENT_FORM
                                : DECLARED_FORM);
      
    case LEFT_CURLY:
      n = Statements(t, x);
      t.mustMatch(RIGHT_CURLY);
      return n;
      
    case IF:
      // NJS: new Node -> Node
      n = Node(t);
      n.condition = ParenExpression(t, x);
      x.stmtStack.push(n);
      n.thenPart = Statement(t, x);
      n.elsePart = t.match(ELSE) ? Statement(t, x) : null;
      x.stmtStack.pop();
      return n;

    case SWITCH:
      // NJS: new Node -> Node
      n = Node(t);
      t.mustMatch(LEFT_PAREN);
      n.discriminant = Expression(t, x);
      t.mustMatch(RIGHT_PAREN);
      n.cases = [];
      n.defaultIndex = -1;
      x.stmtStack.push(n);
      t.mustMatch(LEFT_CURLY);
      while ((tt = t.get()) != RIGHT_CURLY) {
        switch (tt) {
        case DEFAULT:
          if (n.defaultIndex >= 0)
            throw t.newSyntaxError("More than one switch default");
          // FALL THROUGH
        case CASE:
          // NJS: new Node -> Node
          n2 = Node(t);
          if (tt == DEFAULT)
            n.defaultIndex = n.cases.length;
          else
            n2.caseLabel = Expression(t, x, COLON);
          break;
        default:
          throw t.newSyntaxError("Invalid switch case");
        }
        t.mustMatch(COLON);
        // NJS: new Node -> Node
        n2.statements = Node(t, BLOCK);
        while ((tt=t.peek()) != CASE && tt != DEFAULT && tt != RIGHT_CURLY)
          n2.statements.push(Statement(t, x));
        n.cases.push(n2);
      }
      x.stmtStack.pop();
      return n;

    case FOR:
      // NJS: new Node -> Node
      n = Node(t);
      n.isLoop = true;
      t.mustMatch(LEFT_PAREN);
      if ((tt = t.peek()) != SEMICOLON) {
        x.inForLoopInit = true;
        if (tt == VAR || tt == CONST) {
          t.get();
          n2 = Variables(t, x);
        } else {
          n2 = Expression(t, x);
        }
        x.inForLoopInit = false;
      }
      if (n2 && t.match(IN)) {
        n.type = FOR_IN;
        if (n2.type == VAR) {
          if (n2.length != 1) {
            throw new SyntaxError("Invalid for..in left-hand side",
                                  t.filename, n2.lineno);
          }

          // NB: n2[0].type == IDENTIFIER and n2[0].value == n2[0].name.
          n.iterator = n2[0];
          n.varDecl = n2;
        } else {
          n.iterator = n2;
          n.varDecl = null;
        }
        n.object = Expression(t, x);
      } else {
        n.setup = n2 || null;
        t.mustMatch(SEMICOLON);
        n.condition = (t.peek() == SEMICOLON) ? null : Expression(t, x);
        t.mustMatch(SEMICOLON);
        n.update = (t.peek() == RIGHT_PAREN) ? null : Expression(t, x);
      }
      t.mustMatch(RIGHT_PAREN);
      n.body = nest(t, x, n, Statement);
      return n;

    case WHILE:
      // NJS: new Node -> Node
      n = Node(t);
      n.isLoop = true;
      n.condition = ParenExpression(t, x);
      n.body = nest(t, x, n, Statement);
      return n;

    case DO:
      // NJS: new Node -> Node
      n = Node(t);
      n.isLoop = true;
      n.body = nest(t, x, n, Statement, WHILE);
      n.condition = ParenExpression(t, x);
      if (!x.ecmaStrictMode) {
        // <script language="JavaScript"> (without version hints) may need
        // automatic semicolon insertion without a newline after do-while.
        // See http://bugzilla.mozilla.org/show_bug.cgi?id=238945.
        t.match(SEMICOLON);
        return n;
      }
      break;

    case BREAK:
    case CONTINUE:
      // NJS: new Node -> Node
      n = Node(t);
      if (t.peekOnSameLine() == IDENTIFIER) {
        t.get();
        // NJS: -> token()
        n.label = t.token().value;
      }
      ss = x.stmtStack;
      i = ss.length;
      label = n.label;
      if (label) {
        do {
          if (--i < 0)
            throw t.newSyntaxError("Label not found");
        } while (ss[i].label != label);
      } else {
        do {
          if (--i < 0) {
            throw t.newSyntaxError("Invalid " + ((tt == BREAK)
                                                 ? "break"
                                                 : "continue"));
          }
        } while (!ss[i].isLoop && (tt != BREAK || ss[i].type != SWITCH));
      }
      n.target = ss[i];
      break;

    case TRY:
      // NJS: new Node -> Node
      n = Node(t);
      n.tryBlock = Block(t, x);
      n.catchClauses = [];
      while (t.match(CATCH)) {
        // NJS: new Node -> Node
        n2 = Node(t);
        t.mustMatch(LEFT_PAREN);
        n2.varName = t.mustMatch(IDENTIFIER).value;
        if (t.match(IF)) {
          if (x.ecmaStrictMode)
            throw t.newSyntaxError("Illegal catch guard");
          if (n.catchClauses.length && !n.catchClauses.top().guard)
            throw t.newSyntaxError("Guarded catch after unguarded");
          n2.guard = Expression(t, x);
        } else {
          n2.guard = null;
        }
        t.mustMatch(RIGHT_PAREN);
        n2.block = Block(t, x);
        n.catchClauses.push(n2);
      }
      if (t.match(FINALLY))
        n.finallyBlock = Block(t, x);
      if (!n.catchClauses.length && !n.finallyBlock)
        throw t.newSyntaxError("Invalid try statement");
      return n;

    case CATCH:
    case FINALLY:
      throw t.newSyntaxError(tokens[tt] + " without preceding try");

    // Stratified suspend/retract/finally block:
    case SUSPEND:
      n = Node(t);
      n.suspendBlock = Block(t, x);
      if (t.match(RETRACT))
        n.retractBlock = Block(t, x);
      if (t.match(FINALLY))
        n.finallyBlock = Block(t, x);
      return n;

    case RETRACT:
      throw t.newSyntaxError("retract without preceding suspend");
      
    case THROW:
      // NJS: new Node -> Node
      n = Node(t);
      n.exception = Expression(t, x);
      break;

    case RETURN:
      if (!x.inFunction)
        throw t.newSyntaxError("Invalid return");
      // NJS: new Node -> Node
      n = Node(t);
      tt = t.peekOnSameLine();
      if (tt != END && tt != NEWLINE && tt != SEMICOLON && tt != RIGHT_CURLY)
        n.value = Expression(t, x);
      break;

    case WITH:
      // NJS: new Node -> Node
      n = Node(t);
      n.object = ParenExpression(t, x);
      n.body = nest(t, x, n, Statement);
      return n;

    case VAR:
    case CONST:
      n = Variables(t, x);
      break;

    case DEBUGGER:
      // NJS: new Node -> Node
      n = Node(t);
      break;

    case NEWLINE:
    case SEMICOLON:
      // NJS: new Node -> Node
      n = Node(t, SEMICOLON);
      n.expression = null;
      return n;

    default:
      if (tt == IDENTIFIER) {
        t.scanOperand = false;
        tt = t.peek();
        t.scanOperand = true;
        if (tt == COLON) {
          // NJS: -> token()
          label = t.token().value;
          ss = x.stmtStack;
          for (i = ss.length-1; i >= 0; --i) {
            if (ss[i].label == label)
              throw t.newSyntaxError("Duplicate label");
          }
          t.get();
          // NJS: new Node -> Node
          n = Node(t, LABEL);
          n.label = label;
          n.statement = nest(t, x, n, Statement);
          return n;
        }
      }

      // NJS: new Node -> Node
      n = Node(t, SEMICOLON);
      t.unget();
      n.expression = Expression(t, x);
      n.end = n.expression.end;
      break;
    }
    
    // NJS: -> token()
    if (t.lineno == t.token().lineno) {
      tt = t.peekOnSameLine();
      if (tt != END && tt != NEWLINE && tt != SEMICOLON && tt != RIGHT_CURLY)
        throw t.newSyntaxError("Missing ; before statement");
    }
    t.match(SEMICOLON);
    return n;
  }

  function FunctionDefinition(t, x, requireName, functionForm) {
    // NJS: new Node -> Node
    var f = Node(t);
    if (f.type != FUNCTION)
      f.type = (f.value == "get") ? GETTER : SETTER;
    if (t.match(IDENTIFIER)) {
      // NJS: -> token()
      f.name = t.token().value;
    }
    else if (requireName)
      throw t.newSyntaxError("Missing function identifier");

    t.mustMatch(LEFT_PAREN);
    f.params = [];
    var tt;
    while ((tt = t.get()) != RIGHT_PAREN) {
      if (tt != IDENTIFIER)
        throw t.newSyntaxError("Missing formal parameter");
      // NJS: -> token()
      f.params.push(t.token().value);
      if (t.peek() != RIGHT_PAREN)
        t.mustMatch(COMMA);
    }

    t.mustMatch(LEFT_CURLY);
    var x2 = new CompilerContext(true);
    f.body = Script(t, x2);
    t.mustMatch(RIGHT_CURLY);
    // NJS: -> token()
    f.end = t.token().end;
    
    f.functionForm = functionForm;
    if (functionForm == DECLARED_FORM)
      x.funDecls.push(f);
    return f;
  }

  function Variables(t, x) {
    // NJS: new Node -> Node
    var n = Node(t);
    do {
      t.mustMatch(IDENTIFIER);
      // NJS: new Node -> Node
      var n2 = Node(t);
      n2.name = n2.value;
      if (t.match(ASSIGN)) {
        // NJS: -> token()
        if (t.token().assignOp)
          throw t.newSyntaxError("Invalid variable initialization");
        n2.initializer = Expression(t, x, COMMA);
      }
      n2.readOnly = (n.type == CONST);
      n.push(n2);
      x.varDecls.push(n2);
    } while (t.match(COMMA));
    return n;
  }

  function ParenExpression(t, x) {
    t.mustMatch(LEFT_PAREN);
    var n = Expression(t, x);
    t.mustMatch(RIGHT_PAREN);
    return n;
  }

  var opPrecedence = {
    SEMICOLON: 0,
    COMMA: 1,
    ASSIGN: 2, HOOK: 2, COLON: 2, 
    // The above all have to have the same precedence, see bug 330975.
    ALT: 3, // Stratified Alt operator
    OR: 4,
    AND: 5,
    BITWISE_OR: 6,
    BITWISE_XOR: 7,
    BITWISE_AND: 8,
    EQ: 9, NE: 9, STRICT_EQ: 9, STRICT_NE: 9,
    LT: 10, LE: 10, GE: 10, GT: 10, IN: 10, INSTANCEOF: 10,
    LSH: 11, RSH: 11, URSH: 11,
    PLUS: 12, MINUS: 12,
    MUL: 13, DIV: 13, MOD: 13,
    DELETE: 14, VOID: 14, TYPEOF: 14, // PRE_INCREMENT: 14, PRE_DECREMENT: 14,
    NOT: 14, BITWISE_NOT: 14, UNARY_PLUS: 14, UNARY_MINUS: 14,
    INCREMENT: 15, DECREMENT: 15,     // postfix
    NEW: 16,
    DOT: 17
  };

	// Map operator type code to precedence.
	// NJS EDIT: slurp opPrecence items into array first, because IE includes
	//           modified hash items in iterator when modified during iteration
	var opPrecedenceItems = [];
	for (i in opPrecedence) 
		opPrecedenceItems.push(i);
	
	for (var i = 0; i < opPrecedenceItems.length; i++) {
		var item = opPrecedenceItems[i];
		opPrecedence[eval(item)] = opPrecedence[item];
	}

  var opArity = {
    COMMA: -2,
    ALT: -2,
    ASSIGN: 2,
    HOOK: 3,
    OR: 2,
    AND: 2,
    BITWISE_OR: 2,
    BITWISE_XOR: 2,
    BITWISE_AND: 2,
    EQ: 2, NE: 2, STRICT_EQ: 2, STRICT_NE: 2,
    LT: 2, LE: 2, GE: 2, GT: 2, IN: 2, INSTANCEOF: 2,
    LSH: 2, RSH: 2, URSH: 2,
    PLUS: 2, MINUS: 2,
    MUL: 2, DIV: 2, MOD: 2,
    DELETE: 1, VOID: 1, TYPEOF: 1,  // PRE_INCREMENT: 1, PRE_DECREMENT: 1,
    NOT: 1, BITWISE_NOT: 1, UNARY_PLUS: 1, UNARY_MINUS: 1,
    INCREMENT: 1, DECREMENT: 1,     // postfix
    NEW: 1, NEW_WITH_ARGS: 2, DOT: 2, INDEX: 2, CALL: 2,
    ARRAY_INIT: 1, OBJECT_INIT: 1, GROUP: 1
  };

	// Map operator type code to arity.
	// NJS EDIT: same as above
	var opArityItems = [];
	for (i in opArity)
		opArityItems.push(i);
	
	for (var i = 0; i < opArityItems.length; i++) {
		var item = opArityItems[i];
		opArity[eval(item)] = opArity[item];
	}
  
  function Expression(t, x, stop) {
    var n, id, tt, operators = [], operands = [];
    var bl = x.bracketLevel, cl = x.curlyLevel, pl = x.parenLevel,
             hl = x.hookLevel;

    function reduce() {
      var n = operators.pop();
      var op = n.type;
      var arity = opArity[op];
      if (arity == -2) {
        // Flatten left-associative trees.
        var left = operands.length >= 2 && operands[operands.length-2];
        if (left.type == op) {
          var right = operands.pop();
          left.push(right);
          return left;
        }
        arity = 2;
      }

      // Always use push to add operands to n, to update start and end.
			// NJS EDIT: provide second argument to splice or IE won't work.
      var index = operands.length - arity;
      var a = operands.splice(index, operands.length - index);
      for (var i = 0; i < arity; i++)
        n.push(a[i]);
      
      // Include closing bracket or postfix operator in [start,end).
      // NJS: -> token()
      if (n.end < t.token().end)
        n.end = t.token().end;
      
      operands.push(n);
      return n;
    }

    loop:
    while ((tt = t.get()) != END) {
      if (tt == stop &&
          x.bracketLevel == bl && x.curlyLevel == cl && x.parenLevel == pl &&
          x.hookLevel == hl) {
        // Stop only if tt matches the optional stop parameter, and that
        // token is not quoted by some kind of bracket.
        break;
      }
      switch (tt) {
      case SEMICOLON:
        // NB: cannot be empty, Statement handled that.
        break loop;
        
      case ASSIGN:
      case HOOK:
      case COLON:
        if (t.scanOperand)
          break loop;
        // Use >, not >=, for right-associative ASSIGN and HOOK/COLON.
        while (opPrecedence[operators.top().type] > opPrecedence[tt] ||
               (tt == COLON && operators.top().type == ASSIGN)) {
          reduce();
        }
        if (tt == COLON) {
          n = operators.top();
          if (n.type != HOOK)
            throw t.newSyntaxError("Invalid label");
          --x.hookLevel;
        } else {
          // NJS: new Node -> Node
          operators.push(Node(t));
          if (tt == ASSIGN) {
            // NJS: -> token()
            operands.top().assignOp = t.token().assignOp;
          }
          else
            ++x.hookLevel;      // tt == HOOK
        }
        t.scanOperand = true;
        break;

      case IN:
        // An in operator should not be parsed if we're parsing the head of
        // a for (...) loop, unless it is in the then part of a conditional
        // expression, or parenthesized somehow.
        if (x.inForLoopInit && !x.hookLevel &&
            !x.bracketLevel && !x.curlyLevel && !x.parenLevel) {
          break loop;
        }
        // FALL THROUGH
      case COMMA:
        // Treat comma as left-associative so reduce can fold left-heavy
        // COMMA trees into a single array.
        // FALL THROUGH
      case ALT: // Stratified Alt operator
      case OR:
      case AND:
      case BITWISE_OR:
      case BITWISE_XOR:
      case BITWISE_AND:
      case EQ: case NE: case STRICT_EQ: case STRICT_NE:
      case LT: case LE: case GE: case GT:
      case INSTANCEOF:
      case LSH: case RSH: case URSH:
      case PLUS: case MINUS:
      case MUL: case DIV: case MOD:
      case DOT:
        if (t.scanOperand)
          break loop;
        while (opPrecedence[operators.top().type] >= opPrecedence[tt])
          reduce();
        if (tt == DOT) {
          t.mustMatch(IDENTIFIER);
          // NJS: new Node -> Node
          operands.push(Node(t, DOT, operands.pop(), Node(t)));
        } else {
          // NJS: new Node -> Node
          operators.push(Node(t));
          t.scanOperand = true;
        }
        break;
        
      case DELETE: case VOID: case TYPEOF:
      case NOT: case BITWISE_NOT: case UNARY_PLUS: case UNARY_MINUS:
      case NEW:
        if (!t.scanOperand)
          break loop;
        // NJS: new Node -> Node
        operators.push(Node(t));
        break;

      case INCREMENT: case DECREMENT:
        if (t.scanOperand) {
          // NJS: new Node -> Node
          operators.push(Node(t));  // prefix increment or decrement
        } else {
          // Don't cross a line boundary for postfix {in,de}crement.
          if (t.tokens[(t.tokenIndex + t.lookahead - 1) & 3].lineno !=
              t.lineno) {
            break loop;
          }
          
          // Use >, not >=, so postfix has higher precedence than prefix.
          while (opPrecedence[operators.top().type] > opPrecedence[tt])
            reduce();
          // NJS: new Node -> Node
          n = Node(t, tt, operands.pop());
          n.postfix = true;
          operands.push(n);
        }
        break;

      case FUNCTION:
        if (!t.scanOperand)
          break loop;
        operands.push(FunctionDefinition(t, x, false, EXPRESSED_FORM));
        t.scanOperand = false;
        break;

      case NULL: case THIS: case TRUE: case FALSE:
      case IDENTIFIER: case NUMBER: case STRING: case REGEXP:
        if (!t.scanOperand)
          break loop;
        // NJS: new Node -> Node
        operands.push(Node(t));
        t.scanOperand = false;
        break;

      case LEFT_BRACKET:
        if (t.scanOperand) {
          // Array initialiser.  Parse using recursive descent, as the
          // sub-grammar here is not an operator grammar.
          // NJS: new Node -> Node
          n = Node(t, ARRAY_INIT);
          while ((tt = t.peek()) != RIGHT_BRACKET) {
            if (tt == COMMA) {
              t.get();
              n.push(null);
              continue;
            }
            n.push(Expression(t, x, COMMA));
            if (!t.match(COMMA))
              break;
          }
          t.mustMatch(RIGHT_BRACKET);
          operands.push(n);
          t.scanOperand = false;
        } else {
          // Property indexing operator.
          // NJS: new Node -> Node
          operators.push(Node(t, INDEX));
          t.scanOperand = true;
          ++x.bracketLevel;
        }
        break;

      case RIGHT_BRACKET:
        if (t.scanOperand || x.bracketLevel == bl)
          break loop;
        while (reduce().type != INDEX)
          continue;
        --x.bracketLevel;
        break;
        
      case LEFT_CURLY:
        if (!t.scanOperand)
          break loop;
        // Object initialiser.  As for array initialisers (see above),
        // parse using recursive descent.
        ++x.curlyLevel;
        // NJS: new Node -> Node
        n = Node(t, OBJECT_INIT);
        object_init:
        if (!t.match(RIGHT_CURLY)) {
          do {
            tt = t.get();
            // NJS: -> token()
            if ((t.token().value == "get" || t.token().value == "set") &&
                t.peek() == IDENTIFIER) {
              if (x.ecmaStrictMode)
                throw t.newSyntaxError("Illegal property accessor");
              n.push(FunctionDefinition(t, x, true, EXPRESSED_FORM));
            } else {
              switch (tt) {
              case IDENTIFIER:
              case NUMBER:
              case STRING:
                // NJS: new Node -> Node
                id = Node(t);
                break;
              case RIGHT_CURLY:
                if (x.ecmaStrictMode)
                  throw t.newSyntaxError("Illegal trailing ,");
                break object_init;
              default:
                throw t.newSyntaxError("Invalid property name");
              }
              t.mustMatch(COLON);
              // NJS: new Node -> Node
              n.push(Node(t, PROPERTY_INIT, id,
                          Expression(t, x, COMMA)));
            }
          } while (t.match(COMMA));
          t.mustMatch(RIGHT_CURLY);
        }
        operands.push(n);
        t.scanOperand = false;
        --x.curlyLevel;
        break;
        
      case RIGHT_CURLY:
        if (!t.scanOperand && x.curlyLevel != cl)
          throw "PANIC: right curly botch";
        break loop;
        
      case LEFT_PAREN:
        if (t.scanOperand) {
          // NJS: new Node -> Node
          operators.push(Node(t, GROUP));
        } else {
          while (opPrecedence[operators.top().type] > opPrecedence[NEW])
            reduce();
          
          // Handle () now, to regularize the n-ary case for n > 0.
          // We must set scanOperand in case there are arguments and
          // the first one is a regexp or unary+/-.
          n = operators.top();
          t.scanOperand = true;
          if (t.match(RIGHT_PAREN)) {
            if (n.type == NEW) {
              --operators.length;
              n.push(operands.pop());
            } else {
              // NJS: new Node -> Node
              n = Node(t, CALL, operands.pop(),
                       Node(t, LIST));
            }
            operands.push(n);
            t.scanOperand = false;
            break;
          }
          if (n.type == NEW)
            n.type = NEW_WITH_ARGS;
          else {
            // NJS: new Node -> Node
            operators.push(Node(t, CALL));
          }
        }
        ++x.parenLevel;
        break;
        
      case RIGHT_PAREN:
        if (t.scanOperand || x.parenLevel == pl)
          break loop;
        while ((tt = reduce().type) != GROUP && tt != CALL &&
               tt != NEW_WITH_ARGS) {
          continue;
        }
        if (tt != GROUP) {
          n = operands.top();
          if (n[1].type != COMMA) {
            // NJS: new Node -> Node
            n[1] = Node(t, LIST, n[1]);
          }
          else
            n[1].type = LIST;
        }
        --x.parenLevel;
        break;
        
        // Automatic semicolon insertion means we may scan across a newline
        // and into the beginning of another statement.  If so, break out of
        // the while loop and let the t.scanOperand logic handle errors.
      default:
        break loop;
      }
    }

    if (x.hookLevel != hl)
      throw t.newSyntaxError("Missing : after ?");
    if (x.parenLevel != pl)
      throw t.newSyntaxError("Missing ) in parenthetical");
    if (x.bracketLevel != bl)
      throw t.newSyntaxError("Missing ] in index expression");
    if (t.scanOperand)
      throw t.newSyntaxError("Missing operand");
    
    // Resume default mode, scanning for operands, not operators.
    t.scanOperand = true;
    t.unget();
    while (operators.length)
      reduce();
    return operands.pop();
  }

  function parse(s, f, l) {
    var t = new Tokenizer(s, f, l);
    var x = new CompilerContext(false);
    var n = Script(t, x);
    // NJS: -> done()
    if (!t.done())
      throw t.newSyntaxError("Syntax error");
    return n;
  }

  // NJS: make stuff visible
	this.parse      = parse;
	this.Node       = Node;
	this.tokens     = tokens;
	this.consts     = consts;

// END OF NARCISSUS CODE
//-------------------------------

  function indent(ctx) {
    rv = "";
    var i = ctx.indent*2;
    while (i--)
      rv += " ";
    return rv;
  }

  function serializeLVal(n, ctx) {
    if (n.type == tokens.IDENTIFIER)
      return "'" + n.value + "'";
    else
      return serializeNode(n, ctx);
  }
  
  function serializeNode(n, ctx) {
    if (!ctx)
      ctx = { indent : 0 };
    var rv = "";
    switch(n.type) {
      //case tokens['\n']:
    case tokens[';']:
      rv += indent(ctx);
      if (n.expression)
        rv += serializeNode(n.expression, ctx);
      else
        rv += "Oni.Nop()";
      rv += "\n";
      break;
    case tokens[',']:
      rv += "Oni.Seq(";
      for (var i=0; i<n.length; ++i) {
        if (i!=0)
          rv += ", ";
        rv += serializeNode(n[i], ctx);
      }
      rv += ")";
      break;
    case tokens['@']: // Stratified Alt operator
      rv += "Oni.Alt(";
      for (var i=0; i<n.length; ++i) {
        if (i!=0)
          rv += ", ";
        rv += serializeNode(n[i], ctx);
      }
      rv += ")";
      break;
    case tokens['?']:
      rv += "Oni.If(" + serializeNode(n[0], ctx) +
        "," + serializeNode(n[1], ctx) +
        "," + serializeNode(n[2], ctx) +")";
      break;
      //case tokens[':']: --> '?'
    case tokens['||']:
    case tokens['&&']:
    case tokens['|']:
    case tokens['^']:
    case tokens['&']:
    case tokens['===']:
    case tokens['==']:
    case tokens['!==']:
    case tokens['!=']:
    case tokens['<<']:
    case tokens['<=']:
    case tokens['<']:
    case tokens['>>>']:
    case tokens['>>']:
    case tokens['>=']:
    case tokens['>']:
    case tokens['+']:
    case tokens['-']:
    case tokens['*']:
    case tokens['/']:
    case tokens['%']:
      rv += "Oni['" + tokens[n.type] + "']";
      rv += "(" + serializeNode(n[0], ctx) + ", " + serializeNode(n[1], ctx) + ")";
      break;
    case tokens['=']:
      rv += "Oni.Set(";
      rv += serializeLVal(n[0], ctx);
      if (n[0].assignOp) {
        rv += ", Oni['" + tokens[n[0].assignOp] + "']";
        rv += "(" + serializeNode(n[0], ctx) + ", " + serializeNode(n[1], ctx) + "))";
      }
      else {
        rv += "," + serializeNode(n[1], ctx) + ")";
      }
      break;
    case tokens['++']:
      if (n.postfix) {
        // XXX possible var capture here
        rv += "Oni.Let({ __x__: " + serializeNode(n[0], ctx) + "},";
        rv += "Oni.Set(" + serializeLVal(n[0], ctx) + ", ";
        rv += "Oni['+'](Oni.Get('__x__'), 1)), Oni.Get('__x__'))";
      }
      else {
        rv += "Oni.Set(" + serializeLVal(n[0], ctx) + ", ";
        rv += "Oni['+'](" + serializeNode(n[0], ctx) + ", 1))";
      }
      break;     
    case tokens['--']:
      if (n.postfix) {
        // XXX possible var capture here
        rv += "Oni.Let({ __x__: " + serializeNode(n[0], ctx) + "},";
        rv += "Oni.Set(" + serializeLVal(n[0], ctx) + ", ";
        rv += "Oni['-'](Oni.Get('__x__'), 1)), Oni.Get('__x__'))";
      }
      else {
        rv += "Oni.Set(" + serializeLVal(n[0], ctx) + ", ";
        rv += "Oni['-'](" + serializeNode(n[0], ctx) + ", 1))";
      }
      break;
    case tokens['!']:
    case tokens['~']:
      rv += "Oni['u_" + tokens[n.type] + "']";
      rv += "(" + serializeNode(n[0], ctx) + ")";
      break;
    case tokens.UNARY_PLUS:
      rv += "Oni['u_+']";
      rv += "(" + serializeNode(n[0], ctx) + ")";
      break;
    case tokens.UNARY_MINUS:
      rv += "Oni['u_-']";
      rv += "(" + serializeNode(n[0], ctx) + ")";
      break;
    case tokens['.']:
      rv += "Oni.ObjRef(" + serializeNode(n[0], ctx) + ",'" + n[1].value +"')";
      break;
      //case tokens['[']: --> ARRAY_INIT | INDEX
      //case tokens[']']: --> ARRAY_INIT | INDEX
      //case tokens['{']: --> OBJECT_INIT | BLOCK
      //case tokens['}']: --> OBJECT_INIT | BLOCK
      //case tokens['(']: --> GROUP | LIST
      //case tokens[')']: --> GROUP | LIST
    case tokens.SCRIPT:
      var first = true;
      rv += "Oni.Seq(";
      // variable declarations:
      if (n.varDecls.length) {
        rv += "Oni.CreateBindings([";
        for (var i=0; i<n.varDecls.length; ++i) {
          if (i!=0) rv += ",";
          rv += "'" + n.varDecls[i].name + "'";
        }
        rv += "])";
        first = false;
      }
      // body:
      for (var i=0; i<n.length; ++i) {
        if (!first) rv += ",";
        first = false;
        rv += serializeNode(n[i], ctx);
      }
      rv += ")";
      break;
    case tokens.BLOCK:
      rv += "Oni.Seq(";
      for (var i=0; i<n.length; ++i) {
        if (i!=0) rv += ", ";
        rv += serializeNode(n[i], { indent: ctx.indent+1 });
      }
      rv += ")\n";
      break;
    case tokens.LABEL:
      rv += indent(ctx);
      rv += n.label + ": ";
      rv += serializeNode(n.statement, { indent: 0 });
      break;
    case tokens.FOR_IN:
      rv += indent(ctx);
      rv += "for(var " + serializeNode(n.iterator, ctx) + " in " +
        serializeNode(n.object, ctx) + ")\n";
      rv += serializeNode(n.body, { indent: ctx.indent + 1 });
      break;
    case tokens.CALL:
      // special case built-in Stratified functions here:
      // Stratified hold() operator:
      if (n[0].value == "hold") {
        if (n[1].length > 0)
          rv += "Oni.Sleep(" + serializeNode(n[1], ctx) + ")";
        else
          rv += "Oni.Stop()";
      }
      else {
        rv += "Oni.Apply("+serializeNode(n[0], ctx);
        if (n[1].length > 0) {
          rv += ", ";
          rv += serializeNode(n[1], ctx);
        }
        rv += ")";
      }
      break;
    case tokens.NEW_WITH_ARGS:
      rv += "Oni.NewWithArgs(" + serializeNode(n[0], ctx) + ", ";
      rv += serializeNode(n[1], ctx) + ")";
      break;
    case tokens.INDEX:
      rv += "Oni.ObjRef("
      rv += serializeNode(n[0], ctx);
      rv += ',' + serializeNode(n[1], ctx) + ')';
      break;
	  case tokens.ARRAY_INIT:
      rv += 'Oni.List(';
      for (var i=0; i<n.length; ++i) {
        if (i!=0)
          rv += ", ";
        rv += serializeNode(n[i], ctx);
      }
      rv += ')';
      break;    
    case tokens.OBJECT_INIT:
      rv += "Oni.Obj(";
      for (var i=0; i<n.length; ++i) {
        if (i!=0)
          rv += ", ";
        rv += serializeNode(n[i], ctx);
      }
      rv += ')';
      break;    
    case tokens.PROPERTY_INIT:
      rv += "'" + n[0].value + "'," + serializeNode(n[1], ctx);
      break;
      //case tokens.GETTER:
      //case tokens.SETTER:    
	  case tokens.GROUP:
      // XXX can a group have no children?
      // XXX can a group have more than one child?
      rv += "(" + serializeNode(n[0], ctx) +")";
      break;
    case tokens.LIST: // argument list
      for (var i=0; i<n.length; ++i) {
        if (i!=0)
          rv += ", ";
        rv += serializeNode(n[i], ctx);
      }
      break;
	  case tokens.IDENTIFIER:
      rv += "Oni.Get('"+n.value+"')";
      break;
    case tokens.NUMBER:
      rv += n.value;
      break;
    case tokens.STRING:
      var val = n.value.replace(/(\\|")/g, "\\$1"); // "))
      val = val.replace(/\n/g, "\\n");
      rv += '"' + val + '"';
      break;
    case tokens.REGEXP:
      rv += n.value;
      break;
	  case tokens["break"]:
      rv += "Oni.Break()";
      //XXX TODO: support for labels
      // if (n.label)
      // ...
      break;
	    //case tokens["case"]:
      //case tokens["catch"]:
      //case tokens["const"]:
    case tokens["continue"]:
      rv += "Oni.Continue()";
      break;
	    //case tokens["debugger"]:
      //case tokens["default"]:
      //case tokens["delete"]:
    case tokens["do"]:
      rv += "Oni.Loop(" + serializeNode(n.body, ctx) + ", ";
      rv += "Oni.If(Oni.Not(" + serializeNode(n.condition, ctx);
      rv += "), Oni.Break()))";
      break;
	    //case tokens["else"]:
      //case tokens["enum"]:
	  case tokens["false"]:
      rv += "false";
      break;
      //case tokens["finally"]:
    case tokens["for"]:
      rv += "Oni.Seq(";
      if (n.setup) {
        rv += serializeNode(n.setup) + ", ";
      }
      rv += "Oni.Loop(";
      if (n.condition) {
        rv += "Oni.If(Oni.Not(" + serializeNode(n.condition) + "), Oni.Break()), ";
      }
      rv += "Oni.Catch([Oni.tag_Continue],";
      rv += serializeNode(n.body);
      rv += ")";
      if (n.update) {
        rv += ", " + serializeNode(n.update);
      }
      rv += "))";
      break;
    case tokens["function"]:
      if (n.name !== undefined)
        rv += "Oni.Set('" + n.name + "', ";
      rv += "Oni.Lambda([";
      for (var i=0; i<n.params.length; ++i) {
        if (i!=0) rv += ",";
        rv += "'" + n.params[i] + "'";
      }
      rv += "],\n";
      // afri: XXX until Oni.Return() is implemented, we need this tail-safety-breaking hack :-( 
      rv += "Oni.Catch(['__return__'], ";
      var l = rv.length;
      rv += serializeNode(n.body, { indent: ctx.indent+1 });
      if (l == rv.length)
        rv += "Oni.Nop()";
      if (n.name !== undefined) rv += ")";
      rv += ")"; // afri: XXX parenthesis for Catch hack
      rv += ")\n";
      break;
	  case tokens["if"]:
      rv += "Oni.If(";
      rv += serializeNode(n.condition, ctx);
      rv += ", ";
      rv += serializeNode(n.thenPart, ctx);
      if (n.elsePart != null) {
        rv += ", " + serializeNode(n.elsePart, ctx);
      }
      rv += ")";
      break;
      //case tokens["in"]:
      //case tokens["instanceof"]:
	  case tokens["new"]:
      rv += "Oni.New(" + serializeNode(n[0], ctx) + ")";
      break;
    case tokens["null"]:
      rv += "null";
      break;
	  case tokens["return"]:
      // XXX afri: implement Oni.Return (difficult because we want to be tail-recursive)
      //rv += "Oni.Return(";
      //if (n.value != "return")
      //  rv += serializeNode(n.value, ctx);
      //rv += ")";
      rv += "Oni.Throw('__return__'";
      if (n.value != "return") 
        rv += "," + serializeNode(n.value, ctx);
      rv += ")";
      break;
    case tokens["suspend"]:
      // XXX afri: This implementation in terms of ALift is a bit fragile. I'm sure
      // there is a race condition between calling the suspendblock and retractblock
      rv += "Oni.Let({ resume:null,\n__suspend__: Oni.Lambda([], ";
      rv += serializeNode(n.suspendBlock, ctx);
      rv += "),\n__retract__: Oni.Lambda([], ";
      if (n.retractBlock)
        rv += serializeNode(n.retractBlock, ctx);
      else
        rv += "Oni.Nop()";
      rv += "),\n__finally__: Oni.Lambda([], ";
      if (n.finallyBlock)
        rv += serializeNode(n.finallyBlock, ctx);
      else
        rv += "Oni.Nop()";
      rv += ")},\nOni.Bracket(Oni.Nop(),Oni.SLift(Oni.ALift)(Oni.Lambda(['cont'],";
      rv += "Oni.Set('resume', Oni.Lambda([], Oni.Get('cont')([true, true]))),";
      rv += "Oni.Get('__suspend__')()), Oni.Get('__retract__'))(), Oni.Get('__finally__')()))";
      break;
	  case tokens["switch"]:
      rv += "Oni.Catch([Oni.tag_Break], Oni.Let({__found__:false, __discriminant__:";
      rv += serializeNode(n.discriminant);
      rv += "}";
      for (var i=0; i<n.cases.length; ++i) {
        if (n.cases[i].type == tokens["case"]) {
          rv += ",Oni.If(Oni.Equals(Oni.Get('__discriminant__')," + serializeNode(n.cases[i].caseLabel) + "), Oni.Set('__found__', true)), Oni.If(Oni.Get('__found__'), ";
          rv += serializeNode(n.cases[i].statements) + ")";
        }
        // else ...  type == default handled below
      }
      if (n.defaultIndex != -1) {
        // XXX this is not quite correct for pathological cases... see testcase
        rv += ","+serializeNode(n.cases[n.defaultIndex].statements);
      }
      rv += "))";
      break;
	  case tokens["this"]:
      rv += "Oni.This()";
      break;
      //case tokens["throw"]:
    case tokens["true"]:
      rv += "true";
      break;
    case tokens["try"]:
      // XXX add support for catch
      rv += "Oni.Bracket(Oni.Nop(), " + serializeNode(n.tryBlock, ctx) + ",";
      if (n.finallyBlock)
        rv += serializeNode(n.finallyBlock, ctx);
      else
        rv += "Oni.Nop()";
      rv += ")";
      break;
    case tokens["typeof"]:
      rv += "Oni.Typeof(" + serializeNode(n[0], ctx) + ")";
      break;
	  case tokens["var"]:
      rv += indent(ctx);
      rv += "Oni.Seq(";
      var first = true;
      for (var i=0; i<n.length; ++i) {
        if (!n[i].initializer) continue;
        if (!first) rv += ", ";
        first = false;
        rv += "Oni.Set('" + n[i].name + "', ";
        rv += serializeNode(n[i].initializer, ctx);
        rv += ")";
      }
      rv += ")\n"
      break;
    case tokens["void"]:
      rv += "void " + serializeNode(n[0], ctx);
      break;
	  case tokens["while"]:
      rv += "Oni.Loop(Oni.If(Oni.Not(";
      rv += serializeNode(n.condition, ctx);
      rv += "), Oni.Break()), " + serializeNode(n.body, ctx) + ")";
      break;
      //case tokens["with"]:
    default:
      throw new Error("Unexpected token:\n"+n);
    }
    return rv;
  }
  
  function compile(s) {
    var rv = "";
    rv += "void Oni.Eval("
    rv += serializeNode(parse(s));
    rv += ", this);"
    return rv;
  }

  this.compile = compile;
  
}).call(SJS);

  
function runSJS(s) {
  eval(SJS.compile(s));
}

/*
  Ajax bootstrapping code; js helper code that cannot (yet) be
  expressed easily in SJS
*/

// spawns (SJS) function 'f' in the background
function spawn(f) {
  f();
}

var Ajax = {};

//----------------------------------------------------------------------

Ajax.constructURI = function(/* baseuri, [opt] params1, [opt] params2, ... */) {
  var rv = arguments[0];
  var first = ( rv.indexOf("?") == -1 );
  for (var i=1; i<arguments.length; ++i) {
    var params = arguments[i];
    if (!params) continue;
    for (var p in params) {
      if (first) {
        rv += "?";
        first = false;
      }
      else
        rv += "&";
      rv += encodeURIComponent(p) + "=" + encodeURIComponent(params[p]);
    }
  }
  return rv;
};runSJS("/*\n  Ajax bootstrapping code\n\n*/\n\n// bound in sjs-ajax-bootstrap.js\n// var Ajax = {};\n\n//----------------------------------------------------------------------\n// helpers\n\n// implemented in sjs-ajax-bootstrap.js (pending SJS implementation of for-in)\n//Ajax.constructURI = function(baseuri, properties) \n  \n\n//----------------------------------------------------------------------\n// loading scripts\n\nAjax._pendingScripts = {};\nAjax._loadedScripts = {};\n\nAjax.loadScript = function(url) {\n  if (this._loadedScripts[url])\n    return;\n  var hook = this._pendingScripts[url];\n  \n  if (hook != null) {\n    suspend {\n      hook.push(resume);\n    }\n    //    retract {\n    // XXX could remove resume function from hook here\n    //    }\n    \n  }\n  else {\n    // we're the inital requester\n    var THIS=this; // XXX bug workaround; see http://www.croczilla.com/stratified\n    \n    suspend {\n      var elem = document.createElement(\"script\");\n      var hook = [];\n      THIS._pendingScripts[url] = hook;\n      \n      function listener(e) {\n        resume();\n      }\n      \n      function listenerIE(e) {\n        if (e.srcElement.readyState == \"loaded\" ||\n            e.srcElement.readyState == \"complete\")\n          resume();\n      }\n      \n      if (elem.addEventListener)\n        elem.addEventListener(\"load\", listener, false);\n      else // IE\n        elem.attachEvent(\"onreadystatechange\", listenerIE);\n      \n      // kick off the load:\n      elem.src = url;\n      document.getElementsByTagName(\"head\")[0].appendChild(elem);\n    }\n    retract {\n      THIS._pendingScripts[url] = null;\n    }\n    finally {\n      if (elem.removeEventListener)\n        elem.removeEventListener(\"load\", listener, false);\n      else\n        elem.detachEvent(\"onreadystatechange\", listenerIE);\n    }\n    \n    this._pendingScripts[url] = null;\n    this._loadedScripts[url] = true;\n    for (var i=0; i<hook.length; ++i)\n      hook[i]();\n  }\n};\n\nAjax.loadSJS = function(url) {\n  Ajax.loadScript(\"http://uk.croczilla.com/proxy/compile?script=\" + url);\n};\n\n//----------------------------------------------------------------------\n// requests\n\nAjax.requestJSONP = function(url, params, callback_parameter) {\n  var cbparam = {};\n  cbparam[callback_parameter ? callback_parameter : \"callback\"] = \"R\";  \n  url = Ajax.constructURI(url, cbparam, params);\n  \n  var iframe = document.createElement(\"iframe\");\n  document.getElementsByTagName(\"head\")[0].appendChild(iframe);\n  var rv;\n  suspend {\n    var doc = iframe.contentWindow.document;\n    doc.open();\n    iframe.contentWindow.R = function(data) { rv = data; resume(); };\n    doc.write(\"\x3Cscript type='text/javascript' src='\"+url+\"'>\x3C/script>\");\n    doc.close();\n  }\n  finally {\n    iframe.parentNode.removeChild(iframe);\n  }\n  \n  return rv;\n};\n\n//----------------------------------------------------------------------\n// DOM helpers:\n\nAjax.DOM = {};\n\nAjax.DOM.waitForEvent = function(event, elem) {\n  if (typeof elem == \"string\")\n    elem = document.getElementById(elem);\n  \n  suspend {\n    var rv;\n    var listener_func = function(e) { rv = e; resume(); }\n    if (elem.addEventListener)\n      elem.addEventListener(event, listener_func, false);\n    else // IE\n      elem.attachEvent(\"on\"+event, listener_func);\n  }\n  finally {\n    if (elem.removeEventListener)\n      elem.removeEventListener(event, listener_func, false);\n    else // IE\n      elem.detachEvent(\"on\"+event, listener_func);\n  }\n\n  return rv;\n};\n\n  \n//----------------------------------------------------------------------\n// Google API wrapper:\n\nAjax.google = {};\n\n// ensure that the google ajax api is loaded. Only used internally.\nAjax.google._ensureAPI = function() {\n  Ajax.loadScript(\"http://www.google.com/jsapi\");\n};\n\n// load a particular module through the google api loader\nAjax.google.loadModule = function(moduleName, moduleVersion) {\n  Ajax.google._ensureAPI();\n  suspend {\n    google.load(moduleName, moduleVersion, { callback: resume });\n  }\n};\n\n// low-level wrapper of google search api\n// see http://code.google.com/apis/ajaxsearch/documentation/reference.html#_restUrlBase\n// type parameter: web (default) | local | video | blogs | news | books | images | patent\nAjax.google.search = function(query, /*[opt] */ type, /* [opt] */ extra_params) {\n  var params = { q : query,\n                 v : \"1.0\"\n               };\n  if (!type) type = \"web\";\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/search/\" + type,\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\n\nAjax.google.feed = {};\n\n// low-level wrappers of google feed api\n// see http://code.google.com/apis/ajaxfeeds/documentation/reference.html#_restUrlBase\nAjax.google.feed.load = function(query, /* [opt] */ extra_params) {\n  var params = { q : query,\n                 v : \"1.0\"\n               };\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/feed/load\",\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\nAjax.google.feed.find = function(query, /* [opt] */ extra_params) {\n  var params = { q : query,\n                 v : \"1.0\"\n               };\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/feed/find\",\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\nAjax.google.feed.lookup = function(query, /* [opt] */ extra_params) {\n  var params = { q : query,\n                 v : \"1.0\"\n               };\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/feed/lookup\",\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\n\n// deprecated method that loads feeds through the google API\nAjax.google.feed.loadFeed = function(url, numEntries) {\n  Ajax.google.loadModule(\"feeds\", \"1\");\n  var feed = new google.feeds.Feed(url);\n  feed.setNumEntries(numEntries ? numEntries : 20);\n  var result;\n  suspend {\n    feed.load(function(res) { result = res; resume(); });\n  }\n  \n  return result;\n};\n\nAjax.google.language = {};\n\n// low-level wrappers of google language api\n// see http://code.google.com/apis/ajaxlanguage/documentation/reference.html#_intro_fonje\n\n// src_lang can be null or \"\", in which case the src language will be\n// autodetected\nAjax.google.language.translate = function(text, dest_lang, src_lang, /* [opt] */ extra_params) {\n  if (src_lang == null) src_lang = \"\";\n  var params = { q : text,\n                 v : \"1.0\",\n                 langpair : src_lang + \"|\" + dest_lang\n               };\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/language/translate\",\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\n\nAjax.google.language.detect = function(text, /* [opt] */ extra_params) {\n  var params = { q : text,\n                 v : \"1.0\"\n               };\n  var url = Ajax.constructURI(\"http://ajax.googleapis.com/ajax/services/language/detect\",\n                              params, extra_params);\n  return Ajax.requestJSONP(url);\n};\n");
/*
 Stratified JS loader v0.3
*/
function runScripts() {
  var scripts = document.getElementsByTagName("script");
  for (var i=0; i<scripts.length; ++i) {
    if (scripts[i].type == "text/sjs")
      runSJS(scripts[i].innerHTML);
  }
}

if (window.addEventListener)
  window.addEventListener("load", runScripts, true);
else
  window.attachEvent("onload", runScripts);


